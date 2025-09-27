from django.urls import path
from .views import RevenueCatWebhookView

urlpatterns = [
    path("webhook/revenuecat/", RevenueCatWebhookView.as_view(), name="revenuecat-webhook"),
]
