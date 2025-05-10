# countries_api/urls_web.py
from django.urls import path
from . import views_web

app_name = 'countries_web'  # Optional: Define an app namespace

urlpatterns = [
    path('countries/', views_web.country_list_view, name='country_list_web'),
    # If you want a dedicated URL for the app root, e.g., http://127.0.0.1:8000/web/
    # path('', views_web.country_list_view, name='home_web'),
]