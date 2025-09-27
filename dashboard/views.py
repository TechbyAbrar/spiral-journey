from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from dashboard.serializers import DashboardUserSerializer
from dashboard.services import UserService


class DashboardUserListView(APIView):
    """
    Dashboard API for listing users with search + pagination
    """

    def get(self, request):
        search = request.query_params.get("search")
        page = int(request.query_params.get("page", 1))
        per_page = int(request.query_params.get("per_page", 10))

        users_qs = UserService.list_users(search)
        paginator = Paginator(users_qs, per_page)

        if page > paginator.num_pages or page <= 0:
            return Response(
                {"error": "Invalid page number"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        page_obj = paginator.page(page)

        # Create SL mapping
        start_index = page_obj.start_index()
        index_map = {
            user.user_id: start_index + idx
            for idx, user in enumerate(page_obj.object_list, start=0)
        }

        serializer = DashboardUserSerializer(
            page_obj.object_list, many=True, context={"index_map": index_map}
        )
        
        # Get verified/unverified counts
        total_verified, total_unverified = UserService.count_verified_unverified()

        return Response(
            {
                "count": paginator.count,
                "total_pages": paginator.num_pages,
                "current_page": page,
                "per_page": per_page,
                "total_verified_user": total_verified,
                "unverified_user": total_unverified,
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
