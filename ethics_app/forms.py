from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, Div, HTML
# from captcha.fields import ReCaptchaField  # Commented out for now
from .models import DataSubjectRequest, ConsentRecord

class ConsentForm(forms.Form):
    functional_cookies = forms.BooleanField(
        required=False,
        label=_('Functional Cookies'),
        help_text=_('Required for website functionality')
    )
    analytics_cookies = forms.BooleanField(
        required=False,
        label=_('Analytics Cookies'),
        help_text=_('Help us improve our website')
    )
    marketing_cookies = forms.BooleanField(
        required=False,
        label=_('Marketing Cookies'),
        help_text=_('For personalized advertising')
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML('<h4>Cookie Preferences</h4>'),
            'functional_cookies',
            'analytics_cookies',
            'marketing_cookies',
            Submit('submit', _('Save Preferences'), css_class='btn btn-primary')
        )

class DataSubjectRequestForm(forms.ModelForm):
    # captcha = ReCaptchaField()  # Commented out for now

    class Meta:
        model = DataSubjectRequest
        fields = ['request_type', 'email', 'full_name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            'request_type',
            'email',
            'full_name',
            'description',
            # 'captcha',  # Commented out
            Submit('submit', _('Submit Request'), css_class='btn btn-primary')
        )

class CookieSettingsForm(forms.Form):
    analytics_enabled = forms.BooleanField(required=False, label=_('Analytics'))
    marketing_enabled = forms.BooleanField(required=False, label=_('Marketing'))
    functional_enabled = forms.BooleanField(required=False, label=_('Functional'))
