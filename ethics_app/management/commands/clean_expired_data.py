### 2. GDPR Compliance Command: ethics_app/management/commands/cleanup_expired_data.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from ethics_app.models import ConsentRecord, DataSubjectRequest
from django.conf import settings

class Command(BaseCommand):
    help = 'Clean up expired consent records and old data subject requests'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting',
        )
        parser.add_argument(
            '--days',
            type=int,
            default=getattr(settings, 'DATA_RETENTION_DAYS', 365),
            help='Number of days to retain data (default: 365)',
        )
    
    def handle(self, *args, **options):
        cutoff_date = timezone.now() - timedelta(days=options['days'])
        dry_run = options['dry_run']
        
        # Find expired consent records
        expired_consents = ConsentRecord.objects.filter(
            expiry_date__lt=timezone.now()
        )
        
        # Find old data subject requests (completed/rejected > retention period)
        old_requests = DataSubjectRequest.objects.filter(
            created_at__lt=cutoff_date,
            status__in=['completed', 'rejected']
        )
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {expired_consents.count()} '
                    f'expired consent records'
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    f'DRY RUN: Would delete {old_requests.count()} '
                    f'old data subject requests'
                )
            )
        else:
            deleted_consents = expired_consents.count()
            deleted_requests = old_requests.count()
            
            expired_consents.delete()
            old_requests.delete()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {deleted_consents} expired consent records'
                )
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully deleted {deleted_requests} old data subject requests'
                )
            )
