from django.shortcuts import render, redirect, get_object_or_404

from app.models import Konfig


def konfigs(request):
    konfigs = Konfig.objects.all()
    return render(request, 'konfigs.html', {'records': konfigs})
