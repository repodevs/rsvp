from django.urls import path

from . import views as v

urlpatterns = [
    # API endpoint
    path('configs/', v.konfig.api_configs, name='api_configs'),
]