# countries_api/views.py
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

# Import DRF authentication and permission classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Country
from .serializers import CountrySerializer

class CountryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows countries to be viewed or edited.
    Requires authentication for all actions.
    """
    queryset = Country.objects.all().order_by('name_common')
    serializer_class = CountrySerializer
    lookup_field = 'cca2'
    
    # --- Authentication and Permissions ---
    authentication_classes = [SessionAuthentication, BasicAuthentication] # Allows session-based (for web) and basic auth (for testing/simple API clients)
    permission_classes = [IsAuthenticated] # Only authenticated users can access
    # --- End Authentication and Permissions ---

    filter_backends = [filters.SearchFilter]
    search_fields = ['name_common', 'name_official']

    # ... (rest of your existing actions: regional_countries, by_language) ...
    @action(detail=True, methods=['get'], url_path='regional-countries')
    def regional_countries(self, request, cca2=None):
        """
        List countries in the same region as the specified country.
        """
        try:
            country = self.get_object()
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
        
        # Using PostgreSQL's JSONB __has_key for efficiency if applicable
        # For general compatibility, ensure your JSONField can be queried efficiently
        # or consider alternative data modeling if performance is critical here.
        # For this assignment, we'll assume a method that works across DBs, even if slower.
        
        # countries_qs = Country.objects.filter(languages__has_key=lang_code.lower()) # Ideal for PostgreSQL
        
        # General approach for broader DB compatibility:
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