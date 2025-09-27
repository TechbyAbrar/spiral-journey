from django.urls import path
from .views import SpiralListCreateView, SpiralDetailView, SpiralDayView, SpiralReflectionView, SoundscapeView, AdminSoundscapeCreateView

urlpatterns = [
    path("spirals/", SpiralListCreateView.as_view(), name="spiral-list-create"),
    path("spirals/<int:pk>/", SpiralDetailView.as_view(), name="spiral-detail"),
    path("spirals/<int:spiral_id>/days/", SpiralDayView.as_view(), name="spiral-day-create"),
    path("spirals/<int:spiral_id>/days/<int:day_id>/", SpiralDayView.as_view(), name="spiral-day-create"),
    
    path("spirals/<int:spiral_id>/days/<int:day_id>/", SpiralDayView.as_view(), name="spiral-day-detail"),
    path("spiral-reflections/", SpiralReflectionView.as_view(), name="spiral-reflection-create"),
    
    path('create-kunchi-soundescapes/', AdminSoundscapeCreateView.as_view(), name='admin-soundscape-create'),
    path('kunchi-soundescapes/', SoundscapeView.as_view(), name='soundscape-list-create'),
]
