from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ethics_app.models import ConsentRecord, DataSubjectRequest
import json

class Command(BaseCommand):
    help = 'Export all data for a specific user (GDPR Article 20)'
    
    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User email address')
        parser.add_argument(
            '--format',
            choices=['json', 'csv'],
            default='json',
            help='Export format',
        )
    
    def handle(self, *args, **options):
        try:
            user = User.objects.get(email=options['email'])
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User with email {options["email"]} not found')
            )
            return
        
        # Collect user data
        user_data = {
            'personal_information': {
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'date_joined': user.date_joined.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
            },
            'consent_records': list(
                ConsentRecord.objects.filter(user=user).values(
                    'consent_type', 'consent_given', 'timestamp', 'legal_basis'
                )
            ),
            'data_subject_requests': list(
                DataSubjectRequest.objects.filter(email=user.email).values(
                    'request_type', 'description', 'status', 'created_at'
                )
            ),
            'export_timestamp': timezone.now().isoformat(),
        }
        
        # Convert datetime objects to strings
        for consent in user_data['consent_records']:
            consent['timestamp'] = consent['timestamp'].isoformat()
        
        for request in user_data['data_subject_requests']:
            request['created_at'] = request['created_at'].isoformat()
        
        if options['format'] == 'json':
            self.stdout.write(json.dumps(user_data, indent=2))
        else:
            # CSV format implementation would go here
            self.stdout.write('CSV export not implemented yet')
