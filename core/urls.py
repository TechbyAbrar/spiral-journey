"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/account/', include('account.urls')),
    path('v1/onboarding/', include('onboarding.urls')),  
    path('v1/privacy-policy/', include('privacy_policy.urls')), 
    path('v1/spiral-journey/', include('spiral_journey.urls')), 
    path('v1/webnote/', include('webnote.urls')),  
    path('v1/monthly-mirror/', include('monthly_mirror.urls')), 
    path('v1/dashboard/', include('dashboard.urls')),
    path('v1/administration/', include('administration.urls')),
    path('v1/subscription/', include('subscription.urls')),
    path('v1/notifications/', include('notification.urls')),  # Notification URLs
]

# Serve static and media only in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)