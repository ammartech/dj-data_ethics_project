from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Count, Q
from ethics_app.models import ConsentRecord, DataSubjectRequest, DataBreach
import json
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate privacy compliance report'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--format',
            choices=['json', 'text'],
            default='text',
            help='Output format (default: text)',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=30,
            help='Report period in days (default: 30)',
        )
    
    def handle(self, *args, **options):
        end_date = timezone.now()
        start_date = end_date - timedelta(days=options['days'])
        
        # Consent statistics
        consent_stats = ConsentRecord.objects.filter(
            timestamp__gte=start_date
        ).values('consent_type').annotate(
            total=Count('id'),
            granted=Count('id', filter=Q(consent_given=True))
        )
        
        # Data subject requests
        request_stats = DataSubjectRequest.objects.filter(
            created_at__gte=start_date
        ).values('request_type', 'status').annotate(count=Count('id'))
        
        # Data breaches
        breach_count = DataBreach.objects.filter(
            detection_date__gte=start_date
        ).count()
        
        # Prepare report data
        report_data = {
            'report_period': {
                'start_date': start_date.isoformat(),
                'end_date': end_date.isoformat(),
                'days': options['days']
            },
            'consent_statistics': list(consent_stats),
            'data_subject_requests': list(request_stats),
            'data_breaches': breach_count,
            'generated_at': timezone.now().isoformat()
        }
        
        if options['format'] == 'json':
            self.stdout.write(json.dumps(report_data, indent=2))
        else:
            self._print_text_report(report_data)
    
    def _print_text_report(self, data):
        self.stdout.write(self.style.SUCCESS('=== PRIVACY COMPLIANCE REPORT ==='))
        self.stdout.write(f"Period: {data['report_period']['start_date']} to {data['report_period']['end_date']}")
        self.stdout.write('')
        
        self.stdout.write(self.style.HTTP_INFO('Consent Statistics:'))
        for stat in data['consent_statistics']:
            consent_rate = (stat['granted'] / stat['total'] * 100) if stat['total'] > 0 else 0
            self.stdout.write(f"  {stat['consent_type']}: {stat['granted']}/{stat['total']} ({consent_rate:.1f}%)")
        
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO('Data Subject Requests:'))
        for req in data['data_subject_requests']:
            self.stdout.write(f"  {req['request_type']} ({req['status']}): {req['count']}")
        
        self.stdout.write('')
        self.stdout.write(self.style.HTTP_INFO(f"Data Breaches: {data['data_breaches']}"))
