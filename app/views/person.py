from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from app.models import Person
from app.forms import PersonForm
from app.utils import paginate_queryset



def persons(request):
    query = request.GET.get('q')
    if query:
        persons = Person.objects.filter(Q(name__icontains=query) | Q(code__icontains=query))
    else:
        persons = Person.objects.all()

    persons = paginate_queryset(request, persons, per_page=10)
    return render(request, 'persons.html', {'records': persons})

def person_detail(request, person_id):
    person = Person.objects.get(id=person_id)
    return render(request, 'person_detail.html', {'person': person})

def person_add(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            person = form.save(commit=False)
            person.is_active = True
            person.save()
            messages.success(request, 'Person added successfully!')
            return render(request, 'partials/persons/new_row.html', {'record': person})
            # return redirect('persons')
        print(form.errors)
        print(request.POST)
    # else:
        # form = PersonForm()
    return HttpResponse(status=400)

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

def person_delete(request, person_id):
    person = Person.objects.get(id=person_id)
    if request.method == 'POST':
        person.delete()
        messages.success(request, 'Person deleted successfully!')
        return redirect('persons')
    return render(request, 'person_delete.html', {'person': person})

