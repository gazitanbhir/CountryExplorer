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
    
    # Additional potentially useful fields from JSON (can be added if needed)
    # tld = models.JSONField(null=True, blank=True)
    # latlng = models.JSONField(null=True, blank=True)
    # area = models.FloatField(null=True, blank=True)
    # borders = models.JSONField(null=True, blank=True) # List of cca3 codes
    # demonyms = models.JSONField(null=True, blank=True)
    # continents = models.JSONField(null=True, blank=True)
    # timezones = models.JSONField(null=True, blank=True)
    # coat_of_arms_png_url = models.URLField(max_length=500, null=True, blank=True)
    # coat_of_arms_svg_url = models.URLField(max_length=500, null=True, blank=True)
    # start_of_week = models.CharField(max_length=20, null=True, blank=True)
    # capital_info_latlng = models.JSONField(null=True, blank=True)
    # postal_code_format = models.CharField(max_length=255, null=True, blank=True)
    # postal_code_regex = models.CharField(max_length=255, null=True, blank=True)


    class Meta:
        verbose_name_plural = "Countries"
        ordering = ['name_common']

    def __str__(self):
        return self.name_common