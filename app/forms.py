from  django.contrib.auth.forms import AdminUserCreationForm
from django import forms

from .models import User, Person, RSVP, Comment, Gift, Tracking, Konfig


class CustomUserCreationForm(AdminUserCreationForm):
    """
    A custom user creation form that inherits from the default Django admin user creation form.
    This form is used to create new users in the admin interface.
    """
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            # 'mobile',
            'password1',
            'password2',
        )
        

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['code', 'name', 'title', 'is_multi_gift', 'is_active']
