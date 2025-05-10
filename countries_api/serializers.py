# countries_api/serializers.py
from rest_framework import serializers
from .models import Country

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__' # You can list specific fields if you prefer
        # Example for specific fields:
        # fields = ['cca2', 'name_common', 'name_official', 'capital', 'region', 
        #           'subregion', 'languages', 'currencies', 'population', 
        #           'flag_png_url', 'flag_svg_url', 'flag_alt_text']
        # lookup_field = 'cca2' # If you want to use cca2 in URLs directly for lookup