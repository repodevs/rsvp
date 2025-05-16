from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AdminUserCreationForm

from .models import RSVP, Person, Comment, Gift, Tracking, Konfig
from .forms import CustomUserCreationForm, PersonForm
from .utils import is_user_or_staff


# Create your views here.

def index(request):
    return redirect('app_home')

@login_required
def app_home(request):
    total_persons = Person.objects.count()
    total_rsvps = RSVP.objects.count()
    total_comments = Comment.objects.count()
    total_gifts = Gift.objects.count()
    data = {
        'total_persons': total_persons,
        'total_rsvps': total_rsvps,
        'total_comments': total_comments,
        'total_gifts': total_gifts
    }
    return render(request, 'index.html', {**data})

