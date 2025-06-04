from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from app.utils import paginate_queryset, download_csv
from app.models import Tracking


@login_required
def tracking(request):
    query = request.GET.get('q')
    if query:
        trackings = Tracking.objects.filter(
            Q(ip__icontains=query) | Q(code__icontains=query)
        ).order_by('-created_at')
    else:
        trackings = Tracking.objects.order_by('-created_at').all()
    trackings = paginate_queryset(request, trackings, per_page=10)
    return render(request, 'trackings.html', {'records': trackings})

@login_required
def tracking_delete(request, tracking_id):
    tracking = get_object_or_404(Tracking, id=tracking_id)
    if request.method == 'POST':
        tracking.delete()
        return redirect('tracking')
    return redirect('tracking')

@login_required
def tracking_download(request):
    query = request.GET.get('q')
    if query:
        trackings = Tracking.objects.filter(
            Q(ip__icontains=query) | Q(code__icontains=query)
        ).order_by('-created_at')
    else:
        trackings = Tracking.objects.order_by('-created_at').all()
    fields = ['id', 'code', 'ip', 'browser_info', 'is_active', 'created_at']
    return download_csv(request, trackings, fields)
