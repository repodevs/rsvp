from django.shortcuts import render, redirect, get_object_or_404

from app.models import Tracking


def tracking(request):
    trackings = Tracking.objects.all()
    return render(request, 'trackings.html', {'records': trackings})
