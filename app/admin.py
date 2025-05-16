from django.apps import apps
from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Person, RSVP, Comment, Gift, Tracking, Konfig, User


class UserAdmin(ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'is_active']
    
    search_fields = ['email', 'first_name', 'last_name']
    
    list_filter = ['is_active', 'role']

admin.site.register(User, UserAdmin)

# Patch for Sorting Model
def get_app_list(self, request, app_label=None):
    """
    Return a sorted list of all the installed apps that have been
    registered in this site.
    """
    app_dict = self._build_app_dict(request, app_label)

    # Sort the apps alphabetically.
    app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

    # Sort the models alphabetically within each app.
    # for app in app_list:
    #     app["models"].sort(key=lambda x: x["name"])

    return app_list

admin.AdminSite.get_app_list = get_app_list


class PersonAdmin(ModelAdmin):
    # fields = ['code', 'name', 'title', 'is_multi_gift']
    add_fieldsets = (
        (None, {'fields': ('code', 'name', 'title', 'is_multi_gift')}),
    )
    fieldsets = (
        (None, {'fields': ('is_active', 'code', 'name', 'title', 'is_multi_gift', 'created_at', 'updated_at')}),
    )
    readonly_fields = ['created_at', 'updated_at']
    list_display = ['code', 'name', 'is_multi_gift', 'updated_at']
    list_filter = ['is_multi_gift']
    search_fields = ['code', 'name']
    ordering = ['created_at']


admin.site.register(Person, PersonAdmin)


class RSVPAdmin(ModelAdmin):
    list_display = ['code', 'name', 'attendance', 'message', 'created_at']

admin.site.register(RSVP, RSVPAdmin)


class CommentAdmin(ModelAdmin):
    list_display = ['name', 'comment', 'created_at']

admin.site.register(Comment, CommentAdmin)


class GiftAdmin(ModelAdmin):
    list_display = ['name', 'message', 'tipe', 'created_at']
    
admin.site.register(Gift, GiftAdmin)



class KonfigAdmin(ModelAdmin):
    list_display = ['key', 'value', 'updated_at']
    
admin.site.register(Konfig, KonfigAdmin)


class TrackingAdmin(ModelAdmin):
    list_display = ['ip', 'browser_info', 'code', 'created_at']

admin.site.register(Tracking, TrackingAdmin)
