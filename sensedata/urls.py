from sensedata import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('debug/', views.debug, name='debug'),
]
