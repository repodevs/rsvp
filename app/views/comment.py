from django.shortcuts import render, redirect, get_object_or_404

from app.models import Comment

def comments(request):
    comments = Comment.objects.all()
    return render(request, 'comments.html', {'records': comments})
