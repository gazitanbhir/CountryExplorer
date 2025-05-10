# countries_api/management/commands/fetch_countries.py
import requests
import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from countries_api.models import Country # Make sure your app name and model name are correct

API_URL = "https://restcountries.com/v3.1/all"

class Command(BaseCommand):
    help = 'Fetches country data from restcountries.com API and stores it in the database.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE(f"Fetching data from {API_URL}..."))
        
        try:
            response = requests.get(API_URL, timeout=60) # Increased timeout for potentially large response
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            countries_data = response.json()
        except requests.exceptions.Timeout:
            raise CommandError(f"Request timed out while fetching data from {API_URL}.")
        except requests.exceptions.RequestException as e:
            raise CommandError(f"Error fetching data from {API_URL}: {e}")
        except json.JSONDecodeError:
            raise CommandError("Error decoding JSON response from API.")
        except Exception as e:
            raise CommandError(f"An unexpected error occurred during API fetch: {e}")


        if not countries_data:
            self.stdout.write(self.style.WARNING("No data received from API."))
            return

        self.stdout.write(self.style.SUCCESS(f"Successfully fetched data for {len(countries_data)} countries."))
        
        countries_created = 0
        countries_updated = 0
        countries_skipped = 0

        # Use a transaction to ensure all or nothing during the database operation
        try:
            with transaction.atomic():
                for country_data in countries_data:
                    # --- Data extraction and cleaning ---
                    name_obj = country_data.get('name', {})
                    common_name = name_obj.get('common')
                    official_name = name_obj.get('official')

                    cca2 = country_data.get('cca2')
                    if not cca2:
                        self.stdout.write(self.style.WARNING(f"Skipping country with missing cca2: {common_name or 'Unknown'}"))
                        countries_skipped += 1
                        continue
                    
                    if not common_name: common_name = cca2 
                    if not official_name: official_name = common_name

                    capitals = country_data.get('capital', []) # API returns a list
                    if not isinstance(capitals, list): capitals = [] # Ensure it's a list, even if API gives something else

                    languages = country_data.get('languages', {}) # API returns a dict
                    if not isinstance(languages, dict): languages = {}

                    currencies_data = country_data.get('currencies', {}) # API returns a dict
                    if not isinstance(currencies_data, dict): currencies_data = {}
                    
                    flags_obj = country_data.get('flags', {})
                    flag_png = flags_obj.get('png')
                    flag_svg = flags_obj.get('svg')
                    flag_alt = flags_obj.get('alt') # Can be None or empty string
                    if flag_alt is None or not str(flag_alt).strip(): # Ensure alt text is not just whitespace
                        flag_alt = f"Flag of {common_name}"

                    coat_of_arms_obj = country_data.get('coatOfArms', {})
                    coat_of_arms_png = coat_of_arms_obj.get('png')
                    coat_of_arms_svg = coat_of_arms_obj.get('svg')
                    
                    postal_code_data = country_data.get('postalCode', {})
                    if not isinstance(postal_code_data, dict): postal_code_data = {}


                    # --- Create or Update ---
                    country_obj, created = Country.objects.update_or_create(
                        cca2=cca2, # Unique identifier to find existing record
                        defaults={
                            'name_common': common_name,
                            'name_official': official_name,
                            'ccn3': country_data.get('ccn3'),
                            'cca3': country_data.get('cca3'),
                            'cioc': country_data.get('cioc'),
                            'capital': capitals,
                            'region': country_data.get('region'),
                            'subregion': country_data.get('subregion'),
                            'languages': languages,
                            'currencies': currencies_data,
                            'population': country_data.get('population'),
                            'flag_png_url': flag_png,
                            'flag_svg_url': flag_svg,
                            'flag_alt_text': flag_alt,
                            # Additional fields from the model
                            'tld': country_data.get('tld', []),
                            'independent': country_data.get('independent'),
                            'status': country_data.get('status'),
                            'un_member': country_data.get('unMember'),
                            'idd': country_data.get('idd', {}),
                            'alt_spellings': country_data.get('altSpellings', []),
                            'latlng': country_data.get('latlng', []),
                            'landlocked': country_data.get('landlocked'),
                            'borders': country_data.get('borders', []),
                            'area': country_data.get('area'),
                            'demonyms': country_data.get('demonyms', {}),
                            'maps': country_data.get('maps', {}),
                            'gini': country_data.get('gini', {}),
                            'fifa': country_data.get('fifa'),
                            'car': country_data.get('car', {}),
                            'timezones': country_data.get('timezones', []),
                            'continents': country_data.get('continents', []),
                            'coat_of_arms_png_url': coat_of_arms_png,
                            'coat_of_arms_svg_url': coat_of_arms_svg,
                            'start_of_week': country_data.get('startOfWeek'),
                            'capital_info': country_data.get('capitalInfo', {}),
                            'postal_code': postal_code_data,
                            'translations': country_data.get('translations', {}),
                        }
                    )

                    if created:
                        countries_created += 1
                    else:
                        countries_updated += 1
                
                self.stdout.write(self.style.SUCCESS(f"Database update complete."))
                self.stdout.write(self.style.SUCCESS(f"Created: {countries_created} countries."))
                self.stdout.write(self.style.SUCCESS(f"Updated: {countries_updated} countries."))
                if countries_skipped > 0:
                    self.stdout.write(self.style.WARNING(f"Skipped: {countries_skipped} countries due to missing cca2."))

        except Exception as e: # Catch any other unexpected errors during DB operation
            raise CommandError(f"An error occurred during database update: {e}")