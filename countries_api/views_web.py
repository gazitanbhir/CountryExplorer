# countries_api/views_web.py
from django.shortcuts import render
from django.db.models import Q
from .models import Country
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required # Import decorator

@login_required # Add this decorator
def country_list_view(request):
    query = request.GET.get('q', '')
    countries_list = Country.objects.all().order_by('name_common')

    if query:
        countries_list = countries_list.filter(
            Q(name_common__icontains=query) |
            Q(name_official__icontains=query) |
            Q(cca2__iexact=query)
        )

    paginator = Paginator(countries_list, 25)
    page_number = request.GET.get('page')
    try:
        countries = paginator.page(page_number)
    except PageNotAnInteger:
        countries = paginator.page(1)
    except EmptyPage:
        countries = paginator.page(paginator.num_pages)

    context = {
        'countries': countries,
        'search_query': query,
        'page_obj': countries,
    }
    return render(request, 'countries_api/country_list.html', context)