"""
URL configuration for rsvp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.shortcuts import redirect

from app import views

urlpatterns = [
    path('app/', include('app.urls')),
    path('api/', include('app.urls_api')),
    
    # use built-in authentication django with custom templates
    path('accounts/', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.user.register, name='register'),
    
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('<str:code>/', views.wedding_home, name='wedding_home'),
    path('<str:code>/qr/', views.person.person_qr_code, name='person_qr_code'),
    path('<str:code>/confirm/', views.rsvp.rsvp_attendance_code, name='rsvp_attendance_code'),
]


def custom_404(request, exception):
    """
    Custom 404 error handler.
    """
    return redirect('index')

handler404 = custom_404
