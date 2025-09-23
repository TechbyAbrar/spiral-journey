from django.urls import path
from .views import SpiralListCreateView, SpiralDetailView, SpiralDayView

urlpatterns = [
    path("spirals/", SpiralListCreateView.as_view(), name="spiral-list-create"),
    path("spirals/<int:pk>/", SpiralDetailView.as_view(), name="spiral-detail"),
    path("spirals/<int:spiral_id>/days/", SpiralDayView.as_view(), name="spiral-day-create"),
    path("spirals/<int:spiral_id>/days/<int:day_id>/", SpiralDayView.as_view(), name="spiral-day-create"),
    
    path("spirals/<int:spiral_id>/days/<int:day_id>/", SpiralDayView.as_view(), name="spiral-day-detail"),
]
