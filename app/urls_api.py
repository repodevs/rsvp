from django.urls import path

from . import views as v

urlpatterns = [
    # API endpoint
    path('configs/', v.konfig.api_configs, name='api_configs'),
    path('rsvp/list/', v.rsvp.api_rsvp_list, name='api_rsvp_list'),
    path('rsvp/<str:code>/confirm/', v.rsvp.api_rsvp_confirm, name='api_rsvp_confirm'),
]