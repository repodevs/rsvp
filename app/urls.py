from django.urls import path

from . import views as v

urlpatterns = [
    path('', v.app_home, name='app_home'),
    path('persons/', v.person.persons, name='persons'),
    path('persons/add/', v.person.person_add, name='person_add'),
    path('persons/<int:person_id>/', v.person.person_detail, name='person_detail'),
    path('persons/<int:person_id>/edit/', v.person.person_edit, name='person_edit'),
    path('persons/<int:person_id>/delete/', v.person.person_delete, name='person_delete'),
    path('persons/download/', v.person.person_download, name='person_download'),

    
    path('rsvps/', v.rsvp.rsvps, name='rsvps'),
    path('rsvps/<int:rsvp_id>/edit/', v.rsvp.rsvp_edit, name='rsvp_edit'),
    path('rsvps/confirm/', v.rsvp.rsvp_confirm, name='rsvp_confirm'),
    path('rsvps/download/', v.rsvp.rsvp_download, name='rsvp_download'),
    
    path('comments/', v.comment.comments, name='comments'),
    path('gifts/', v.gift.gifts, name='gifts'),
    path('konfigs/', v.konfig.konfigs, name='konfigs'),

    path('tracking/', v.tracking.tracking, name='tracking'),
    path('tracking/<int:tracking_id>/delete/', v.tracking.tracking_delete, name='tracking_delete'),
    path('tracking/download/', v.tracking.tracking_download, name='tracking_download'),

    path('users/', v.user.users, name='users'),
    path('users/add/', v.user.user_add, name='user_add'),
    path('users/<int:user_id>/', v.user.user_detail, name='user_detail'),
    path('users/<int:user_id>/edit/', v.user.user_edit, name='user_edit'),
    path('users/<int:user_id>/delete/', v.user.user_delete, name='user_delete'),
    path('users/<int:user_id>/edit_password/', v.user.user_edit_password, name='user_edit_password'),
    path('users/download/', v.user.user_download, name='user_download'),

    path('dashboard/', v.dashboard, name='dashboard'),
    # path('signin/', v.signin, name='signin'),
    
    # API endpoint
    path('api/configs/', v.konfig.api_configs, name='api_configs'),
]