
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from app.models import Gift



@login_required
def gifts(request):
    gifts = Gift.objects.all()
    return render(request, 'gifts.html', {'records': gifts})
