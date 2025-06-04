import csv
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse


def paginate_queryset(request, queryset, per_page=10):
    """
    Paginate a queryset based on the request and the specified number of items per page.
    """
    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page', 1)
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return page_obj


def is_user_or_staff(request, user):
    """
    Check if the request user is the same as the user or if the request user is a staff member.
    """
    return request.user == user or request.user.is_staff


def download_csv(request, objects, fields):
    """
    Generate CSV download response for any model objects.
    
    Args:
        request: Django request object
        objects: QuerySet of objects to export
        fields: List of field names to export
    
    Returns:
        HttpResponse with CSV content
    """
    query = request.GET.get('q')
    
    # Get model name from objects
    model_name = objects.model._meta.model_name.lower()
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{model_name}_{timestamp}.csv"
    
    if query:
        # Sanitize query for filename
        safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
        filename = f"{model_name}_{safe_query}_{timestamp}.csv"
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    
    # Create headers from field names (uppercase)
    headers = [field.upper() for field in fields]
    writer.writerow(headers)
    
    # Write data rows
    for obj in objects:
        row_data = []
        for field in fields:
            value = getattr(obj, field, '')
            
            # Handle different field types
            if value is None:
                value = ''
            elif hasattr(value, 'strftime'):  # DateTime fields
                value = value.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(value, bool):  # Boolean fields
                value = 'Yes' if value else 'No'
            
            row_data.append(value)
        
        writer.writerow(row_data)
    
    return response
