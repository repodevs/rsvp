from django.shortcuts import render, redirect, get_object_or_404

from app.models import RSVP



def rsvps(request):
    rsvps = RSVP.objects.all()
    return render(request, 'rsvps.html', {'records': rsvps})


