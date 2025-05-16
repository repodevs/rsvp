from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth import get_user_model

from app.forms import CustomUserCreationForm



def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        form.username = request.POST.get('email')
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created successfully!')
            return redirect('login')  # Redirect to the login page
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def users(request):
    # filter is_staff true or false
    users = get_user_model().objects.filter(Q(is_staff=True) | Q(is_staff=False)).all()
    print(users)
    return render(request, 'users.html', {'records': users})


def user_detail(request, user_id):
    user = get_user_model().objects.get(id=user_id)
    return render(request, 'user_detail.html', {'user': user})

def user_edit(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'get_user_model() updated successfully!')
            return redirect('users')
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, 'user_edit.html', {'form': form})

def user_delete(request, user_id):
    user = get_user_model().objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'get_user_model() deleted successfully!')
        return redirect('users')
    return render(request, 'user_delete.html', {'user': user})

def user_edit_password(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, instance=user)
        if form.is_valid():
            form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Password updated successfully!')
            return redirect('users')
    else:
        form = CustomUserCreationForm(instance=user)
    return render(request, 'user_edit_password.html', {'form': form})

