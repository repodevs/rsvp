from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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
