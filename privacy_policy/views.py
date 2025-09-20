


from rest_framework import generics
from .models import PrivacyPolicy, TrustSafety, TermsConditions
from .serializers import (
    PrivacyPolicySerializer, 
    TrustSafetySerializer, 
    TermsConditionsSerializer,
)
from account.permissions import IsSuperUserOrReadOnly
from rest_framework.permissions import AllowAny

class SingleObjectViewMixin:
    """Always returns the first object in the queryset"""
    def get_object(self):
        return self.queryset.first()

class PrivacyPolicyView(SingleObjectViewMixin, generics.RetrieveUpdateAPIView):
    queryset = PrivacyPolicy.objects.all()
    serializer_class = PrivacyPolicySerializer
    permission_classes = [IsSuperUserOrReadOnly]

class TrustSafetyView(SingleObjectViewMixin, generics.RetrieveUpdateAPIView):
    queryset = TrustSafety.objects.all()
    serializer_class = TrustSafetySerializer
    permission_classes = [IsSuperUserOrReadOnly]

class TermsConditionsView(SingleObjectViewMixin, generics.RetrieveUpdateAPIView):
    queryset = TermsConditions.objects.all()
    serializer_class = TermsConditionsSerializer
    permission_classes = [IsSuperUserOrReadOnly]
