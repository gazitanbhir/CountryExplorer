# country_explorer/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView # For redirecting the root URL

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('countries_api.urls')),          # From Phase 2
    path('web/', include('countries_api.urls_web')),     # Our new web URLs
    path('', RedirectView.as_view(url='/web/countries/', permanent=True)), # Redirect root to country list
]