# countries_api/admin.py
from django.contrib import admin
from .models import Country
from django.utils.html import format_html

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name_common', 'cca2', 'region', 'population', 'capital_display', 'flag_preview_list')
    search_fields = ('name_common', 'name_official', 'cca2', 'capital__contains') # For JSONField search
    list_filter = ('region', 'subregion', 'landlocked', 'un_member')
    
    # Fields to display in the detail view (some can be read-only)
    readonly_fields = ('flag_preview_detail', 'coat_of_arms_preview_detail')

    fieldsets = (
        ('Identification', {
            'fields': ('name_common', 'name_official', 'cca2', 'ccn3', 'cca3', 'cioc', 'alt_spellings', 'translations')
        }),
        ('Geography', {
            'fields': ('region', 'subregion', 'continents', 'capital', 'capital_info', 'latlng', 'area', 'landlocked', 'borders', 'maps', 'timezones')
        }),
        ('Demographics & Culture', {
            'fields': ('population', 'languages', 'demonyms', 'gini', 'start_of_week')
        }),
        ('Codes & Status', {
            'fields': ('tld', 'independent', 'status', 'un_member', 'fifa', 'idd', 'car', 'postal_code')
        }),
        ('Visuals', {
            'fields': ('flag_png_url', 'flag_svg_url', 'flag_alt_text', 'flag_preview_detail', 
                       'coat_of_arms_png_url', 'coat_of_arms_svg_url', 'coat_of_arms_preview_detail')
        }),
        ('Currencies', {
            'fields': ('currencies',)
        }),
    )


    def capital_display(self, obj):
        if obj.capital and isinstance(obj.capital, list):
            return ", ".join(obj.capital)
        return "N/A"
    capital_display.short_description = 'Capitals'

    def flag_preview_list(self, obj):
        if obj.flag_svg_url:
            return format_html('<img src="{}" width="50" height="30" style="object-fit:contain;" />', obj.flag_svg_url)
        if obj.flag_png_url: # Fallback to PNG if SVG not available
            return format_html('<img src="{}" width="50" height="30" style="object-fit:contain;" />', obj.flag_png_url)
        return "No flag"
    flag_preview_list.short_description = 'Flag'

    def flag_preview_detail(self, obj):
        if obj.flag_svg_url:
            return format_html('<img src="{}" width="150" style="object-fit:contain;" /> <br/> <a href="{0}" target="_blank">{0}</a>', obj.flag_svg_url)
        if obj.flag_png_url:
            return format_html('<img src="{}" width="150" style="object-fit:contain;" /> <br/> <a href="{0}" target="_blank">{0}</a>', obj.flag_png_url)
        return "No flag image"
    flag_preview_detail.short_description = 'Flag Preview'

    def coat_of_arms_preview_detail(self, obj):
        if obj.coat_of_arms_svg_url:
            return format_html('<img src="{}" width="150" style="object-fit:contain;" /> <br/> <a href="{0}" target="_blank">{0}</a>', obj.coat_of_arms_svg_url)
        if obj.coat_of_arms_png_url:
            return format_html('<img src="{}" width="150" style="object-fit:contain;" /> <br/> <a href="{0}" target="_blank">{0}</a>', obj.coat_of_arms_png_url)
        return "No coat of arms image"
    coat_of_arms_preview_detail.short_description = 'Coat of Arms Preview'