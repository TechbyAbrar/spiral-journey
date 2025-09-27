import logging
from django.utils.dateparse import parse_datetime
from .models import UserSubscription
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

def handle_revenuecat_webhook(payload):
    """
    Process RevenueCat webhook payload and update UserSubscription.
    """
    rc_user_id = payload.get("app_user_id")
    entitlements = payload.get("entitlements", {})
    event = payload.get("event", "")

    try:
        user = User.objects.get(id=rc_user_id)  # or map via email if needed
    except User.DoesNotExist:
        logger.warning(f"User with id={rc_user_id} not found")
        return None

    subscription, _ = UserSubscription.objects.get_or_create(
        user=user,
        revenuecat_user_id=rc_user_id,
        defaults={"raw_payload": payload}
    )

    # Determine if any entitlement is active
    is_active = any(e.get("is_active") for e in entitlements.values())
    start, end = None, None
    for e in entitlements.values():
        if e.get("is_active"):
            start = parse_datetime(e.get("started_at"))
            end = parse_datetime(e.get("expires_at"))
            break

    if is_active:
        subscription.activate(start, end)
    else:
        subscription.deactivate()

    subscription.raw_payload = payload
    subscription.save(update_fields=["raw_payload"])
    logger.info(f"Subscription updated: user={user.email}, active={subscription.is_active}")
    return subscription
