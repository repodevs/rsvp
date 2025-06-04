from  django.contrib.auth.forms import AdminUserCreationForm
from django import forms

from .models import User, Person, RSVP, Comment, Gift, Tracking, Konfig


class CustomUserCreationForm(AdminUserCreationForm):
    """
    A custom user creation form that inherits from the default Django admin user creation form.
    This form is used to create new users in the admin interface.
    If no username is provided, use the email as the username.
    """
    username = forms.CharField(required=False)
    role = forms.CharField(required=False)
    mobile = forms.CharField(required=False)

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'mobile',
            'role',
            'password1',
            'password2',
        )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        if not username and email:
            uname = email
            if email and '@' in email:
                uname = email.split('@')[0]
            cleaned_data['username'] = uname
            self.data = self.data.copy()
            self.data['username'] = uname
        return cleaned_data

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'role', 'password', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['code', 'name', 'title', 'is_multi_gift', 'is_active']

class RSVPForm(forms.ModelForm):
    class Meta:
        model = RSVP
        fields = ['code', 'name', 'message', 'attendance', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = False
