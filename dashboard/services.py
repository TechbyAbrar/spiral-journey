from django.db.models import Q
from account.models import UserAuth
from onboarding.models import UserAnswer


class UserService:
    @staticmethod
    def list_users(search=None):
        """
        Fetch users with optional search filter.
        Optimized with prefetch_related for answers.
        """
        qs = UserAuth.objects.all().prefetch_related("answers__question")

        if search:
            qs = qs.filter(
                Q(full_name__icontains=search)
                | Q(email__icontains=search)
                | Q(contanct_no__icontains=search)
            )
        return qs.order_by("-created_at")
    
    @staticmethod
    def count_verified_unverified():
        total_verified = UserAuth.objects.filter(is_verified=True).count()
        total_unverified = UserAuth.objects.filter(is_verified=False).count()
        return total_verified, total_unverified
