from django.urls import path
from .views import (
    PrivacyPolicyView,
    TrustSafetyView,
    TermsConditionsView,
)

urlpatterns = [
    path('privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy'),
    path('trust-safety/', TrustSafetyView.as_view(), name='trust-safety'),
    path('terms-conditions/', TermsConditionsView.as_view(), name='terms-conditions'),
]
