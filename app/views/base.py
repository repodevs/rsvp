from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from app.models import RSVP, Person, Comment, Gift, Tracking, Konfig


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


def dashboard(request):
    return render(request, 'dashboard.html')
