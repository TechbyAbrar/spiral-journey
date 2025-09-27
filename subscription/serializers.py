from rest_framework import serializers
from .models import UserSubscription

class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = ["user_id", "revenuecat_user_id", "is_subscribed", "is_active", "subscription_start", "subscription_end", "status"]
