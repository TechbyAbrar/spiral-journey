from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class UserSubscription(models.Model):
    """
    Modular subscription model for microservice-style architecture.
    Stores subscription status and RevenueCat payload for audit.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    revenuecat_user_id = models.CharField(max_length=255, null=True, blank=True)
    
    is_subscribed = models.BooleanField(default=False)  # quick access flag
    is_active = models.BooleanField(default=False)      # reflects active entitlement
    
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(max_length=50, default="inactive")  # active, expired, canceled

    raw_payload = models.JSONField(null=True, blank=True)  # store full webhook payload for audit
    updated_at = models.DateTimeField(auto_now=True)

    def activate(self, start=None, end=None):
        self.is_active = True
        self.is_subscribed = True
        self.subscription_start = start
        self.subscription_end = end
        self.status = "active"
        self.save(update_fields=["is_active", "is_subscribed", "subscription_start", "subscription_end", "status", "updated_at"])

    def deactivate(self):
        self.is_active = False
        self.is_subscribed = False
        self.status = "inactive"
        self.subscription_end = None
        self.save(update_fields=["is_active", "is_subscribed", "subscription_end", "status", "updated_at"])

    def __str__(self):
        return f"{self.user.email} - {self.status}"
