from django.urls import path
from .views import SpiralListCreateView, SpiralDetailView, SpiralReflectionView, SoundscapeView, AdminSoundscapeCreateView, AdminSpiralDayDetailView, AdminSpiralDayCreateView

urlpatterns = [
    path("spirals/", SpiralListCreateView.as_view(), name="spiral-list-create"),
    path("spirals/<int:pk>/", SpiralDetailView.as_view(), name="spiral-detail"),
    
    path('admin/spirals/<int:spiral_id>/days/create/', AdminSpiralDayCreateView.as_view(), name='admin_spiral_day_create'),
    
    path(
        "admin/spirals/<int:spiral_id>/days/<int:day_number>/",
        AdminSpiralDayDetailView.as_view(),
        name="admin-spiral-day-detail",
    ),
    
    # parted
    path("spiral-reflections/", SpiralReflectionView.as_view(), name="spiral-reflection-create"),
    path('create-kunchi-soundescapes/', AdminSoundscapeCreateView.as_view(), name='admin-soundscape-create'),
    path('kunchi-soundescapes/', SoundscapeView.as_view(), name='soundscape-list-create'),
]


