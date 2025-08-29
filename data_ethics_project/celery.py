
import os
from celery import Celery
from celery.schedules import crontab

# Set default Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'data_ethics_project.settings')

app = Celery('data_ethics_project')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Periodic tasks
app.conf.beat_schedule = {
    'cleanup-expired-data': {
        'task': 'ethics_app.tasks.cleanup_expired_data',
        'schedule': crontab(hour=2, minute=0),  # Daily at 2 AM
    },
    'monthly-compliance-report': {
        'task': 'ethics_app.tasks.generate_monthly_compliance_report',
        'schedule': crontab(day_of_month=1, hour=3, minute=0),  # Monthly
    },
}
