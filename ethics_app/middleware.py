from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.urls import reverse
from .models import ConsentRecord

class ConsentMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Skip consent check for admin and consent pages
        exempt_paths = [
            '/admin/',
            '/consent/',
            '/privacy-policy/',
            '/static/',
            '/media/',
        ]

        if any(request.path.startswith(path) for path in exempt_paths):
            return None

        # Check if user has given essential consent
        has_consent = False

        if request.user.is_authenticated:
            has_consent = ConsentRecord.objects.filter(
                user=request.user,
                consent_type='functional',
                consent_given=True
            ).exists()
        elif request.session.session_key:
            has_consent = ConsentRecord.objects.filter(
                session_key=request.session.session_key,
                consent_type='functional',
                consent_given=True
            ).exists()

        # Redirect to consent page if no essential consent
        if not has_consent and request.path != reverse('consent_management'):  # Changed this line
            request.session['redirect_after_consent'] = request.get_full_path()
            # For now, just set a flag instead of forcing redirect
            request.needs_consent = True

        return None
