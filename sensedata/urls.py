# Imports
# - Sensedata 
from sensedata import views
# - Django
from django.urls import path

# URL patterns
urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Debug NPS page
    path('debug-nps/', views.debug_nps, name='debug-nps'),
]
