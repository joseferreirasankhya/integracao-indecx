# Imports
# - Sensedata 
from sensedata import views
# - Django
from django.urls import path

# URL patterns
urlpatterns = [
    path('', views.index, name='index'),
    # path('debug-nps/', views.debug_nps, name='debug-nps'),
    path('process-nps/', views.process_nps, name='process-nps'),
]
