from sensedata import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('debug-nps/', views.debug_nps, name='debug-nps'),
]
