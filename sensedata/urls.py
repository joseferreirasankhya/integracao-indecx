# Imports
# - Sensedata 
from sensedata import views

# - Django
from django.urls import path

# URL patterns
urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Debug page
    path('debug/', views.debug, name='debug'),
]
