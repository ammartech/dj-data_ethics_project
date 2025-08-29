from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.mail import send_mail
from django.conf import settings
import json
from .models import ConsentRecord, DataSubjectRequest, PrivacyPolicy
from .forms import ConsentForm, DataSubjectRequestForm, CookieSettingsForm

class HomeView(TemplateView):
    template_name = 'ethics_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['consent_form'] = ConsentForm()
        return context

class PrivacyPolicyView(TemplateView):
    template_name = 'ethics_app/privacy_policy.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = self.request.LANGUAGE_CODE
        try:
            policy = PrivacyPolicy.objects.filter(
                language=language,
                is_active=True
            ).latest('effective_date')
        except PrivacyPolicy.DoesNotExist:
            policy = None
        context['policy'] = policy
        return context

class ConsentManagementView(TemplateView):
    template_name = 'ethics_app/consent_management.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = ConsentForm()

        # Get current consent status
        user_consents = {}
        if self.request.user.is_authenticated:
            consents = ConsentRecord.objects.filter(user=self.request.user)
        else:
            consents = ConsentRecord.objects.filter(
                session_key=self.request.session.session_key
            )

        for consent in consents:
            user_consents[consent.consent_type] = consent.consent_given

        context['form'] = form
        context['current_consents'] = user_consents
        return context

    def post(self, request, *args, **kwargs):
        form = ConsentForm(request.POST)
        if form.is_valid():
            self._save_consents(form.cleaned_data)
            messages.success(request, _('Consent preferences updated successfully.'))
        return redirect('consent_management')

    def _save_consents(self, consent_data):
        from django.utils import timezone
        from datetime import timedelta

        consent_mapping = {
            'functional_cookies': 'functional',
            'analytics_cookies': 'analytics',
            'marketing_cookies': 'marketing',
        }

        for form_field, consent_type in consent_mapping.items():
            consent_given = consent_data.get(form_field, False)

            defaults = {
                'consent_given': consent_given,
                'ip_address': self._get_client_ip(),
                'expiry_date': timezone.now() + timedelta(days=365),
            }

            if self.request.user.is_authenticated:
                ConsentRecord.objects.update_or_create(
                    user=self.request.user,
                    consent_type=consent_type,
                    defaults=defaults
                )
            else:
                ConsentRecord.objects.update_or_create(
                    session_key=self.request.session.session_key,
                    consent_type=consent_type,
                    defaults=defaults
                )

    def _get_client_ip(self):
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip

class DataRequestView(CreateView):
    model = DataSubjectRequest
    form_class = DataSubjectRequestForm
    template_name = 'ethics_app/data_request.html'
    success_url = '/data-request/?success=1'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Send confirmation email
        send_mail(
            subject=_('Data Subject Request Confirmation'),
            message=_('Your request has been received and will be processed within 30 days.'),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[form.cleaned_data['email']],
            fail_silently=True,
        )

        messages.success(
            self.request,
            _('Your request has been submitted successfully.')
        )
        return response

@method_decorator(csrf_exempt, name='dispatch')
class CookieConsentAPIView(TemplateView):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            consent_type = data.get('type')
            consent_given = data.get('consent', False)

            # Save consent record
            ConsentRecord.objects.update_or_create(
                session_key=request.session.session_key,
                consent_type=consent_type,
                defaults={
                    'consent_given': consent_given,
                    'ip_address': self._get_client_ip(request),
                }
            )

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    def _get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
