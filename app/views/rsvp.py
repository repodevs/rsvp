import csv
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from app.forms import RSVPForm
from app.utils import api_validator, paginate_queryset, download_csv
from app.models import RSVP, Person



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

def rsvp_attendance_code(request, code):
    """get or create RSVP by code with attendance is YES"""
    if not code:
        return redirect('index')

    person = Person.objects.filter(code=code).first()
    if not person:
        return redirect('index')

    existing_rsvp = RSVP.objects.filter(code=code).first()
    if existing_rsvp:
        # If RSVP already exists, update attendance to YES
        existing_rsvp.attendance = 'YES'
        existing_rsvp.is_active = True
        existing_rsvp.save()
        return redirect('wedding_home', code=code)

    rsvp = RSVP.objects.create(
        code=code,
        name=person.name,
        message='Confirmed attendance using qr code',
        attendance='YES',
        is_active=True
    )

    return redirect('wedding_home', code=code)

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

@api_validator
def api_rsvp_list(request):
    """
    API endpoint to list RSVPs.
    Returns a JSON response with all RSVPs.
    """
    rsvps = RSVP.objects.all().order_by('-created_at')
    datas = []
    for data in rsvps:
        datas.append({
            'id': data.id,
            'code': data.code,
            'name': data.name,
            'message': data.message,
            'attendance': data.attendance,
            'created_at': data.created_at.isoformat()
        })
    return HttpResponse(json.dumps(datas), content_type='application/json')

@csrf_exempt
@api_validator
def api_rsvp_confirm(request, code):
    """
    API endpoint to confirm RSVP.
    Expects a POST request with 'code' in the body.
    Returns a JSON response with the updated RSVP.
    """
    if request.method == 'POST':
        if not code:
            return HttpResponse(json.dumps({'error': 'Code is required'}), status=400, content_type='application/json')
        
        person = Person.objects.filter(code=code).first()
        if not person:
            return HttpResponse(json.dumps({'error': 'Person not found'}), status=404, content_type='application/json')
        
        existing_rsvp = RSVP.objects.filter(code=code).first()
        if existing_rsvp:
            # If RSVP already exists, update attendance to YES
            existing_rsvp.attendance = 'YES'
            existing_rsvp.is_active = True
            existing_rsvp.save()
            rsvp = existing_rsvp
        else:
            # Create a new RSVP
            rsvp = RSVP.objects.create(
                code=code,
                name=person.name,
                message='Confirmed attendance using APP',
                attendance='YES',
                is_active=True
            )

        response_data = {
            'id': rsvp.id,
            'code': rsvp.code,
            'name': rsvp.name,
            'message': rsvp.message,
            'attendance': rsvp.attendance,
            'created_at': rsvp.created_at.isoformat()
        }
        return HttpResponse(json.dumps(response_data), content_type='application/json')
    
    return HttpResponse(status=405)  # Method Not Allowed