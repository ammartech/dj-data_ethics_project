from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django_countries.fields import CountryField
import uuid

class ConsentRecord(models.Model):
    CONSENT_TYPES = [
        ('functional', 'Functional Cookies'),
        ('analytics', 'Analytics Cookies'),
        ('marketing', 'Marketing Cookies'),
        ('data_processing', 'Data Processing'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    ip_address = models.GenericIPAddressField()
    consent_type = models.CharField(max_length=20, choices=CONSENT_TYPES)
    consent_given = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    expiry_date = models.DateTimeField()
    legal_basis = models.CharField(max_length=100, default='consent')

    class Meta:
        unique_together = ['user', 'session_key', 'consent_type']

class DataSubjectRequest(models.Model):
    REQUEST_TYPES = [
        ('access', 'Data Access'),
        ('rectification', 'Data Rectification'),
        ('erasure', 'Data Erasure'),
        ('portability', 'Data Portability'),
        ('restriction', 'Processing Restriction'),
        ('objection', 'Processing Objection'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    request_type = models.CharField(max_length=20, choices=REQUEST_TYPES)
    email = models.EmailField()
    full_name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    response = models.TextField(blank=True)
class DataProcessingActivity(models.Model):
    name = models.CharField(max_length=200)
    purpose = models.TextField()
    legal_basis = models.CharField(max_length=100)
    data_categories = models.TextField()
    retention_period = models.IntegerField(help_text="Days")
    third_party_sharing = models.BooleanField(default=False)
    cross_border_transfer = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class DataBreach(models.Model):
    BREACH_TYPES = [
        ('confidentiality', 'Confidentiality Breach'),
        ('integrity', 'Integrity Breach'),
        ('availability', 'Availability Breach'),
    ]

    SEVERITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    breach_type = models.CharField(max_length=20, choices=BREACH_TYPES)
    severity = models.CharField(max_length=10, choices=SEVERITY_LEVELS)
    description = models.TextField()
    affected_records = models.IntegerField()
    detection_date = models.DateTimeField(auto_now_add=True)
    notification_required = models.BooleanField(default=True)
    authority_notified = models.BooleanField(default=False)
    subjects_notified = models.BooleanField(default=False)

class PrivacyPolicy(models.Model):
    version = models.CharField(max_length=10)
    content = models.TextField()
    effective_date = models.DateTimeField()
    language = models.CharField(max_length=5, default='en')
    is_active = models.BooleanField(default=False)

    class Meta:
        unique_together = ['version', 'language']
