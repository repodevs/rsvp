import csv
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from app.forms import RSVPForm
from app.utils import paginate_queryset, download_csv
from app.models import RSVP



@login_required
def rsvps(request):
    query = request.GET.get('q')
    if query:
        rsvps = RSVP.objects.filter(name__icontains=query).order_by('name')
    else:
        rsvps = RSVP.objects.order_by('name').all()
    rsvps = paginate_queryset(request, rsvps, per_page=10)
    return render(request, 'rsvps.html', {'records': rsvps})

@login_required
def rsvp_edit(request, rsvp_id):
    rsvp = get_object_or_404(RSVP, id=rsvp_id)
    if request.method == 'POST':
        form = RSVPForm(request.POST, instance=rsvp)
        if form.is_valid():
            form.save()
            return redirect('rsvps')
    else:
        form = RSVPForm(instance=rsvp)
    return redirect('rsvps')

@login_required
def rsvp_confirm(request):
    """
    Confirm RSVP with optional code.
    If 'code' is provided and exists, update the RSVP.
    Otherwise, always create a new RSVP.
    """
    if request.method == 'POST':
        form = RSVPForm(request.POST)
        if form.is_valid():
            form.is_active = True  # Ensure RSVP is active
            code = form.cleaned_data.get('code')
            if code:
                rsvp, created = RSVP.objects.update_or_create(
                    code=code,
                    defaults=form.cleaned_data
                )
            else:
                rsvp = form.save()
            return render(request, 'partials/rsvps/confirm_response.html', {'record': rsvp})
        else:
            return HttpResponse(form.errors.as_text(), status=422)
    return HttpResponse(201)

@login_required
def rsvp_download(request):
    query = request.GET.get('q')
    if query:
        # Search in both name and code fields for better filtering
        rsvps = RSVP.objects.filter(
            Q(name__icontains=query) | Q(code__icontains=query)
        ).order_by('-created_at')
    else:
        rsvps = RSVP.objects.all().order_by('-created_at')
    
    # Define fields to export
    fields = ['id', 'code', 'name', 'message', 'attendance', 'is_active', 'created_at']
    
    return download_csv(request, rsvps, fields)
