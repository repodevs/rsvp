from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import get_user_model

from app.utils import download_csv, paginate_queryset
from app.forms import CustomUserCreationForm, UserForm



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


@login_required
def users(request):
    query = request.GET.get('q')
    if query:
        users = get_user_model().objects.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).all()
    else:
        users = get_user_model().objects.all()
    
    # if not request.user.role == 'admin' filter to only show the current user
    if request.user:
        if not request.user.role == 'ADMIN':
            users = users.filter(id=request.user.id)
    else:
        users = users.exclude(is_superuser=True)
    
    users = users.order_by('first_name', 'last_name')

    users = paginate_queryset(request, users, per_page=10)
    return render(request, 'users.html', {'records': users})


@login_required
def user_detail(request, user_id):
    user = get_user_model().objects.get(id=user_id)
    return render(request, 'user_detail.html', {'user': user})


@login_required
def user_add(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            record = form.save()
            messages.success(request, 'Your account has been created successfully!')
            return render(request, 'partials/users/new_row.html', {'record': record})
    # else:
        # form = CustomUserCreationForm()
    return HttpResponse(form.errors.as_text(), status=422)


@login_required
def user_edit(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('users')
        else:
            messages.error(request, 'Error updating user. Please check the form.')
    else:
        form = UserForm(instance=user)
    # return render(request, 'user_edit.html', {'form': form})
    return redirect('user_detail', user_id=user_id)

@login_required
def user_delete(request, user_id):
    user = get_user_model().objects.get(id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('users')
    return render(request, 'user_delete.html', {'user': user})

@login_required
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

@login_required
def user_download(request):
    query = request.GET.get('q')
    if query:
        users = get_user_model().objects.filter(
            Q(username__icontains=query) | 
            Q(email__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query)
        ).all()
    else:
        users = get_user_model().objects.all()

    fields = ['id', 'username', 'email', 'first_name', 'last_name', 'mobile', 'role', 'is_active', 'date_joined']
    return download_csv(request, users, fields)
