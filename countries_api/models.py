# countries_api/models.py
from django.db import models

class Country(models.Model):
    name_common = models.CharField(max_length=255)
    name_official = models.CharField(max_length=255)
    
    cca2 = models.CharField(max_length=2, unique=True, help_text="2-letter country code ISO 3166-1 alpha-2")
    ccn3 = models.CharField(max_length=3, null=True, blank=True, help_text="3-digit country code ISO 3166-1 numeric")
    cca3 = models.CharField(max_length=3, null=True, blank=True, help_text="3-letter country code ISO 3166-1 alpha-3")
    cioc = models.CharField(max_length=3, null=True, blank=True, help_text="3-letter International Olympic Committee code")

    capital = models.JSONField(null=True, blank=True, help_text="List of capital cities")
    region = models.CharField(max_length=100, null=True, blank=True)
    subregion = models.CharField(max_length=100, null=True, blank=True)
    
    languages = models.JSONField(null=True, blank=True, help_text="Dictionary of languages, e.g., {'eng': 'English'}")
    currencies = models.JSONField(null=True, blank=True, help_text="Dictionary of currencies, e.g., {'USD': {'name': '...', 'symbol': '...'}}")
    
    population = models.PositiveIntegerField(null=True, blank=True)
    
    flag_png_url = models.URLField(max_length=500, null=True, blank=True)
    flag_svg_url = models.URLField(max_length=500, null=True, blank=True)
    flag_alt_text = models.TextField(null=True, blank=True)
    
    # Additional fields that could be useful (from your JSON sample)
    tld = models.JSONField(null=True, blank=True, help_text="Top-level domain(s)")
    independent = models.BooleanField(null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    un_member = models.BooleanField(null=True, blank=True, verbose_name="UN Member")
    idd = models.JSONField(null=True, blank=True, help_text="International direct dialing info")
    alt_spellings = models.JSONField(null=True, blank=True, help_text="Alternative spellings")
    latlng = models.JSONField(null=True, blank=True, help_text="Latitude and Longitude")
    landlocked = models.BooleanField(null=True, blank=True)
    borders = models.JSONField(null=True, blank=True, help_text="List of cca3 codes of bordering countries")
    area = models.FloatField(null=True, blank=True)
    demonyms = models.JSONField(null=True, blank=True)
    # 'flag' field stores unicode emoji, not suitable for direct model field, use flag_png/svg_url
    maps = models.JSONField(null=True, blank=True, help_text="Links to Google Maps and OpenStreetMaps")
    gini = models.JSONField(null=True, blank=True, help_text="Gini coefficient by year") # Gini is often year-specific
    fifa = models.CharField(max_length=10, null=True, blank=True, help_text="FIFA country code")
    car = models.JSONField(null=True, blank=True, help_text="Car signs and side of road")
    timezones = models.JSONField(null=True, blank=True)
    continents = models.JSONField(null=True, blank=True)
    coat_of_arms_png_url = models.URLField(max_length=500, null=True, blank=True, verbose_name="Coat of Arms PNG")
    coat_of_arms_svg_url = models.URLField(max_length=500, null=True, blank=True, verbose_name="Coat of Arms SVG")
    start_of_week = models.CharField(max_length=20, null=True, blank=True)
    capital_info = models.JSONField(null=True, blank=True, help_text="Capital coordinates")
    postal_code = models.JSONField(null=True, blank=True, help_text="Postal code format and regex")
    translations = models.JSONField(null=True, blank=True, help_text="Country name translations")


    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name_common']

    def __str__(self):
        return self.name_common