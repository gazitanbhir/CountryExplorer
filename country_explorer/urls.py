# country_explorer/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('countries_api.urls')),
    path('web/', include('countries_api.urls_web')),

    # Authentication URLs
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # path('', RedirectView.as_view(url='/web/countries/', permanent=False)),
    # Better: Redirect to login if not authenticated, otherwise to the country list
    path('', lambda request: RedirectView.as_view(url='login' if not request.user.is_authenticated else 'countries_web:country_list_web', permanent=False)(request), name='root_redirect'),
]