from sensedata import views
from django.urls import path

# URL patterns
urlpatterns = [
    path('', views.index, name='index'),
    path('process-nps/', views.process_nps, name='process-nps'),
]
