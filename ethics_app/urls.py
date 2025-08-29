from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('privacy-policy/', views.PrivacyPolicyView.as_view(), name='privacy_policy'),
    path('consent/', views.ConsentManagementView.as_view(), name='consent_management'),
    path('data-request/', views.DataRequestView.as_view(), name='data_request'),
    path('api/cookie-consent/', views.CookieConsentAPIView.as_view(), name='cookie_consent_api'),
]
