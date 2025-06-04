from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from app.models import RSVP, Person, Comment, Gift, Tracking, Konfig


def index(request, code=None):
    return wedding_home(request, code=code)
    # return redirect('app_home')


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


def wedding_home(request, code=None):
    if code:
        # track the request with the provided code
        Tracking.track(request, code)

    # Get configurations and convert to dictionary with boolean values
    konfigs_queryset = Konfig.objects.all()
    konfigs = {k.key: k.value == "1" for k in konfigs_queryset}
 
    # Get person data based on code parameter or person_id query param
    person = None
 
    # First try to get person by code if provided in URL
    if code:
        try:
            person = Person.objects.get(code=code)
        except Person.DoesNotExist:
            person = None
    
    # If no person found by code, try person_id from query params
    if not person:
        person_id = request.GET.get('person_id')
        if person_id:
            try:
                person = Person.objects.get(id=person_id)
            except Person.DoesNotExist:
                person = None

    # Get recent RSVPs for display
    rsvps = RSVP.objects.filter(is_active=True).order_by('-created_at')[:10]
    current_rsvp = RSVP.objects.filter(code=code).first()
 
    # Add timeago and comments for each RSVP
    for rsvp in rsvps:
        # Add timeago (you may need to implement this method in your RSVP model)
        # For now, using a simple placeholder
        rsvp.timeago = "beberapa menit yang lalu"
 
        # Get comments for this RSVP (fixed field name)
        rsvp.comments = Comment.objects.filter(rsvp_id=rsvp).order_by('created_at')
        for comment in rsvp.comments:
            comment.timeago = "beberapa menit yang lalu"
 
    context = {
        'konfigs': konfigs,
        'person': person,
        'rsvps': rsvps,
        'current_rsvp': current_rsvp,
        'code': code
    }
 
    return render(request, 'wedding.html', context)
