from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import DataSubjectRequest
import logging
from django.utils import timezone  # Add this line

logger = logging.getLogger(__name__)

@shared_task(bind=True, max_retries=3)
def process_data_subject_request(self, request_id):
    """Process data subject request asynchronously"""
    try:
        request = DataSubjectRequest.objects.get(id=request_id)
        
        # Update status to processing
        request.status = 'processing'
        request.save()
        
        # Simulate processing time
        import time
        time.sleep(2)
        
        # Process based on request type
        if request.request_type == 'access':
            # Generate data export
            response_text = f"Data access request processed for {request.email}"
        elif request.request_type == 'erasure':
            # Perform data deletion
            response_text = f"Data erasure completed for {request.email}"
        else:
            response_text = f"Request type {request.request_type} processed"
        
        # Update request with response
        request.status = 'completed'
        request.response = response_text
        request.processed_at = timezone.now()
        request.save()
        
        # Send notification email
        send_mail(
            subject=f'Your {request.get_request_type_display()} Request - Completed',
            message=f'''
            Dear {request.full_name},
            
            Your data subject request has been completed.
            
            Request ID: {request.id}
            Request Type: {request.get_request_type_display()}
            Status: {request.get_status_display()}
            
            Response: {response_text}
            
            Best regards,
            Data Protection Team
            ''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[request.email],
            fail_silently=False
        )
        
        logger.info(f'Processed data subject request {request_id}')
        
    except DataSubjectRequest.DoesNotExist:
        logger.error(f'Data subject request {request_id} not found')
    except Exception as exc:
        logger.error(f'Error processing request {request_id}: {exc}')
        # Retry the task
        raise self.retry(exc=exc, countdown=60 * (self.request.retries + 1))

@shared_task
def cleanup_expired_data():
    """Cleanup expired data - runs daily"""
    from django.core.management import call_command
    call_command('cleanup_expired_data')

@shared_task  
def generate_monthly_compliance_report():
    """Generate monthly compliance report"""
    from django.core.management import call_command
    call_command('generate_privacy_report', '--days=30', '--format=json')
