
from django.shortcuts import render, redirect, get_object_or_404

from app.models import Gift



def gifts(request):
    gifts = Gift.objects.all()
    return render(request, 'gifts.html', {'records': gifts})
