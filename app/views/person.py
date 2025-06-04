from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse

from app.models import Person
from app.forms import PersonForm
from app.utils import download_csv, paginate_queryset



@login_required
def persons(request):
    query = request.GET.get('q')
    if query:
        persons = Person.objects.filter(Q(name__icontains=query) | Q(code__icontains=query)).order_by('name')
    else:
        persons = Person.objects.order_by('name').all()

    persons = paginate_queryset(request, persons, per_page=10)
    return render(request, 'persons.html', {'records': persons})

@login_required
def person_detail(request, person_id):
    person = Person.objects.get(id=person_id)
    return render(request, 'person_detail.html', {'person': person})

def person_qr_code(request, code):
    person = get_object_or_404(Person, code=code)
    # Generate QR code for the person
    url = request.build_absolute_uri(reverse('wedding_home', kwargs={'code': person.code}))
    data = f'{url}'
    qr_code_url = f"https://api.qrserver.com/v1/create-qr-code/?data={data}&size=200x200"
    return HttpResponse(f"<img src='{qr_code_url}' alt='QR Code for {person.name}' />")

@login_required
def person_add(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.is_active = True
            person.save()
            messages.success(request, 'Person added successfully!')
            # return render(request, 'partials/persons/new_row.html', {'record': person})
            return redirect('persons')
    # else:
        # form = PersonForm()
    return HttpResponse(form.errors.as_text(), status=422)

@login_required
def person_edit(request, person_id):
    # Get the person_id and the request authentication user should same
    # person = Person.objects.get(id=person_id)
    person = get_object_or_404(Person, id=person_id)

    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            messages.success(request, 'Person updated successfully!')
            return redirect('persons')
    else:
        form = PersonForm(instance=person)
    # return render(request, 'person_edit.html', {'form': form})
    return redirect('person_detail', person_id=person_id)

@login_required
def person_delete(request, person_id):
    person = Person.objects.get(id=person_id)
    if request.method == 'POST':
        person.delete()
        messages.success(request, 'Person deleted successfully!')
        return redirect('persons')
    return render(request, 'person_delete.html', {'person': person})

@login_required
def person_download(request):
    query = request.GET.get('q')
    if query:
        persons = Person.objects.filter(
            Q(name__icontains=query) | Q(code__icontains=query)
        ).order_by('-created_at')
    else:
        persons = Person.objects.order_by('-created_at').all()

    fields = ['id', 'code', 'name', 'title', 'is_multi_gift', 'is_active', 'created_at']
    return download_csv(request, persons, fields)
