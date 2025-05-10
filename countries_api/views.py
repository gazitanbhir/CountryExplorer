# countries_api/views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q # For complex lookups

from .models import Country
from .serializers import CountrySerializer

class CountryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows countries to be viewed or edited.
    Provides actions for CRUD operations, as well as custom actions:
    - `regional_countries`: Lists countries in the same region as a specific country.
    - `by_language`: Lists countries where a specific language is spoken (e.g., /api/countries/by_language/?lang_code=eng).
    - Supports searching by `name_common` and `name_official` (e.g., /api/countries/?search=united).
    """
    queryset = Country.objects.all().order_by('name_common')
    serializer_class = CountrySerializer
    lookup_field = 'cca2' # Use cca2 for retrieving specific countries (e.g., /api/countries/US/)
    
    # Add search and filtering capabilities
    filter_backends = [filters.SearchFilter]
    search_fields = ['name_common', 'name_official'] # Fields to search against for ?search=

    # --- Standard CRUD actions are provided by ModelViewSet ---
    # List all countries (GET /api/countries/)
    # Retrieve a specific country (GET /api/countries/{cca2}/)
    # Create a new country (POST /api/countries/)
    # Update an existing country (PUT /api/countries/{cca2}/)
    # Partially update an existing country (PATCH /api/countries/{cca2}/)
    # Delete an existing country (DELETE /api/countries/{cca2}/)

    @action(detail=True, methods=['get'], url_path='regional-countries')
    def regional_countries(self, request, cca2=None):
        """
        List countries in the same region as the specified country.
        """
        try:
            country = self.get_object() # Gets the country instance based on cca2
        except Country.DoesNotExist:
            return Response({"error": "Country not found"}, status=status.HTTP_404_NOT_FOUND)

        if not country.region:
            return Response({"message": "This country does not have region information."}, status=status.HTTP_200_OK)

        regional_countries_qs = Country.objects.filter(region=country.region).exclude(cca2=country.cca2)
        
        page = self.paginate_queryset(regional_countries_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(regional_countries_qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='by-language')
    def by_language(self, request):
        """
        List countries that speak the same language based on a given language code.
        e.g., /api/countries/by-language/?lang_code=eng
        """
        lang_code = request.query_params.get('lang_code', None)
        if not lang_code:
            return Response(
                {"error": "Please provide a 'lang_code' query parameter (e.g., 'eng' for English)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # The languages field is a JSONField like: {"eng": "English", "fra": "French"}
        # We need to check if the provided lang_code is a key in this JSON object.
        # PostgreSQL supports `__has_key` for JSONFields directly:
        # countries_qs = Country.objects.filter(languages__has_key=lang_code)
        
        # For broader database compatibility (e.g., SQLite), we might need to filter in Python,
        # or use a less precise __icontains if storing as a simple string.
        # Let's use a Python-based filter for demonstration if `__has_key` is not available for your DB.
        
        # If using PostgreSQL:
        # countries_qs = Country.objects.filter(languages__has_key=lang_code.lower())
        
        # General approach (potentially less performant on very large datasets without DB specific JSON ops):
        all_countries = Country.objects.all()
        countries_speaking_language = []
        for country in all_countries:
            if country.languages and isinstance(country.languages, dict) and lang_code.lower() in country.languages:
                countries_speaking_language.append(country)
        
        countries_qs = Country.objects.filter(pk__in=[c.pk for c in countries_speaking_language])


        page = self.paginate_queryset(countries_qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(countries_qs, many=True)
        return Response(serializer.data)