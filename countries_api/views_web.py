# countries_api/views_web.py
from django.shortcuts import render
from django.db.models import Q
from .models import Country
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json # Import json

def country_list_view(request):
    query = request.GET.get('q', '')
    countries_list = Country.objects.all().order_by('name_common')

    if query:
        countries_list = countries_list.filter(
            Q(name_common__icontains=query) |
            Q(name_official__icontains=query) |
            Q(cca2__iexact=query)
        )

    # Prepare countries data with JSON string for languages
    # This is a bit inefficient to do for all countries if only a few are clicked.
    # A better approach for large lists might be an AJAX call for the language data itself
    # or a custom serializer if using DRF to render the initial page.
    # For now, this will work for demonstration.
    
    # We'll pass the raw Python dicts to the template and let the template handle it,
    # as serializing here for every country on the page might be less efficient
    # if we can do it correctly in the template. Let's stick to the template fix first.

    paginator = Paginator(countries_list, 25)
    page_number = request.GET.get('page')
    try:
        countries_page = paginator.page(page_number)
    except PageNotAnInteger:
        countries_page = paginator.page(1)
    except EmptyPage:
        countries_page = paginator.page(paginator.num_pages)

    context = {
        'countries': countries_page, # Use the paginated object
        'search_query': query,
        'page_obj': countries_page, 
    }
    return render(request, 'countries_api/country_list.html', context)