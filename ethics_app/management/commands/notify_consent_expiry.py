from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
from ethics_app.models import ConsentRecord

class Command(BaseCommand):
    help = 'Notify users about expiring consent'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--days-ahead',
            type=int,
            default=30,
            help='Notify X days before expiry (default: 30)',
        )
    
    def handle(self, *args, **options):
        notification_date = timezone.now() + timedelta(days=options['days_ahead'])
        
        expiring_consents = ConsentRecord.objects.filter(
            expiry_date__date=notification_date.date(),
            user__isnull=False,
            consent_given=True
        ).select_related('user')
        
        for consent in expiring_consents:
            try:
                send_mail(
                    subject='Your Privacy Preferences Are Expiring',
                    message=f'''
                    Dear {consent.user.get_full_name() or consent.user.username},
                    
                    Your privacy preferences for {consent.consent_type} will expire in {options['days_ahead']} days.
                    
                    Please visit our consent management page to renew your preferences:
                    {settings.SITE_URL}/consent/
                    
                    Best regards,
                    Data Ethics Team
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[consent.user.email],
                    fail_silently=False,
                )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Notified {consent.user.email}')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'Failed to notify {consent.user.email}: {e}')
                )
