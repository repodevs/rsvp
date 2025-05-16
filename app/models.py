"""
Model for the app.

All Model has field `created_by`, `created_at`, `updated_by` and `updated_at`.

- Person: A person who is invited to the event.
    - Code: Unique code for the person. max 50 characters.
    - Name: The name of the person. max 255 characters.
    - Title: The title of the person. e.g: Bapak, Ibu, Saudara, Saudari, Saudara/i.
    - is_multi_gift: The person can bring more than one gift. BOOLEAN. default False.
- RSVP: The RSVP status and Message of a person.
    - Code: (optional) Unique code for the RSVP. max 50 characters.
    - Name: The name of the person. max 255 characters.
    - Message: The message from the person. TEXT NULL.
    - Attendance: The attendances of the person. CHOICES: (YES, NO, MAYBE YES, MAYBE NO).
    - Is_Active: The status of the RSVP. BOOLEAN. default True.
- Comment: A comment to RSVP.
    - rsvp_id: The RSVP ID.
    - Name: The name of the person. max 255 characters.
    - Comment: The comment from the person. TEXT NOT NULL.
- Gift: The gift that a person is bringing to the event.
    - Code: (optional) Unique code for the gift. max 50 characters.
    - Name: The name of the gift. max 255 characters.
    - Message: The message from the person. TEXT NULL.
    - tipe: The type of the gift. CHOICES: (UANG, BARANG).
    - nominal: The nominal of the gift. FLOAT NULL.
    - filename: The filename of the gift. TEXT NULL.
    - content: Binary content of the gift. BLOB NULL.
- Tracking: Link tracking for the RSVP.
    - ip: The IP Address of the person.
    - browser_info: The browser information of the person. TEXT NULL.
    - code: The code of the person. max 50 characters.
    - is_active: The status of the tracking. BOOLEAN. default True.
- Konfig: Configuration for the Invitation.
    - key: The key of the configuration. TEXT NOT NULL UNIQUE.
    - value: The value of the configuration. TEXT NOT NULL.

"""

from django.db import models
from django.contrib.auth.models import AbstractUser, User as CoreUser


# inherit AbstractUser to add field `role`

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'ADMIN'),
        ('STAFF', 'STAFF'),
        ('GUESTBOOK_ATTENDANT', 'GUESTBOOK ATTENDANT'),
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='STAFF')
    mobile = models.CharField(max_length=50, blank=True)

    # inherit createsuperuser to add default role ADMIN
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        return self._create_user(username, email, password, **extra_fields)
    


class Person(models.Model):
    """
    A person who is invited to the event.

    - Code: Unique code for the person. max 50 characters.
    - Name: The name of the person. max 255 characters.
    - Title: The title of the person. e.g: Bapak, Ibu, Saudara, Saudari, Saudara/i.
    - is_multi_gift: The person can bring more than one gift. BOOLEAN. default False.
    """
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255, blank=False)
    title = models.CharField(max_length=50)
    is_multi_gift = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RSVP(models.Model):
    """
    The RSVP status and Message of a person.

    - Code: (optional) Unique code for the RSVP. max 50 characters.
    - Name: The name of the person. max 255 characters.
    - Message: The message from the person. TEXT NULL.
    - Attendance: The attendances of the person. CHOICES: (YES, NO, MAYBE YES, MAYBE NO).
    - Is_Active: The status of the RSVP. BOOLEAN. default True.
    """
    code = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(max_length=255)
    message = models.TextField(null=True, blank=True)
    ATTENDANCE_CHOICES = [
        ('YES', 'YES'),
        ('NO', 'NO'),
        ('MAYBE YES', 'MAYBE YES'),
        ('MAYBE NO', 'MAYBE NO'),
    ]
    attendance = models.CharField(
        max_length=10,
        choices=ATTENDANCE_CHOICES,
        default='MAYBE YES',
    )
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Comment(models.Model):
    """
    A comment to RSVP.

    - rsvp_id: The RSVP ID.
    - Name: The name of the person. max 255 characters.
    - Comment: The comment from the person. TEXT NOT NULL.
    """
    rsvp_id = models.ForeignKey(RSVP, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name


class Gift(models.Model):
    """
    The gift that a person is bringing to the event.

    - Code: (optional) Unique code for the gift. max 50 characters.
    - Name: The name of the gift. max 255 characters.
    - Message: The message from the person. TEXT NULL.
    - tipe: The type of the gift. CHOICES: (UANG, BARANG).
    - nominal: The nominal of the gift. FLOAT NULL.
    - filename: The filename of the gift. TEXT NULL.
    - content: Binary content of the gift. BLOB NULL.
    """
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    name = models.CharField(max_length=255)
    message = models.TextField(null=True, blank=True)
    TIPE_CHOICES = [
        ('UANG', 'UANG'),
        ('BARANG', 'BARANG'),
    ]
    tipe = models.CharField(
        max_length=10,
        choices=TIPE_CHOICES,
        default='UANG',
    )
    nominal = models.FloatField(null=True, blank=True)
    filename = models.CharField(max_length=255, null=True, blank=True)
    content = models.BinaryField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name
    

class Tracking(models.Model):
    """
    Link tracking for the RSVP.

    - ip: The IP Address of the person.
    - browser_info: The browser information of the person. TEXT NULL.
    - code: The code of the person. max 50 characters.
    - is_active: The status of the tracking. BOOLEAN. default True.
    """
    ip = models.GenericIPAddressField(blank=True, null=True)
    browser_info = models.TextField(null=True, blank=True)
    code = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.ip


class Konfig(models.Model):
    """
    Configuration for the Invitation.

    - key: The key of the configuration. TEXT NOT NULL UNIQUE.
    - value: The value of the configuration. TEXT NOT NULL.
    """
    key = models.TextField(unique=True)
    value = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['key']

    def __str__(self):
        return self.key


