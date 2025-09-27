from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from .services import handle_revenuecat_webhook
import hmac, hashlib
from django.conf import settings
import json
import logging

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class RevenueCatWebhookView(APIView):
    """
    Public webhook endpoint to process RevenueCat events.
    """

    authentication_classes = []  # no auth, RevenueCat calls directly
    permission_classes = []

    def post(self, request):
        body = request.body
        signature = request.headers.get("X-RevenueCat-Signature")
        secret = getattr(settings, "REVENUECAT_WEBHOOK_SECRET", "")

        # verify HMAC SHA256 signature
        if secret:
            mac = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
            if not hmac.compare_digest(mac, signature):
                logger.warning("RevenueCat webhook signature mismatch")
                return Response({"error": "Invalid signature"}, status=403)

        try:
            payload = json.loads(body)
        except Exception:
            logger.exception("Invalid JSON payload from RevenueCat")
            return Response({"error": "Invalid JSON"}, status=400)

        subscription = handle_revenuecat_webhook(payload)
        if not subscription:
            return Response({"error": "User not found"}, status=404)

        return Response({"status": "ok"}, status=200)
