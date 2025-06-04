from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from app.models import Comment

@login_required
def comments(request):
    comments = Comment.objects.all()
    return render(request, 'comments.html', {'records': comments})
