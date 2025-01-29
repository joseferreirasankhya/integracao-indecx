from sensedata import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('ping/', views.ping, name='ping'),
]

