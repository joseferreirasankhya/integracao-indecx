from zendesk import views
from django.urls import path

# URL patterns
urlpatterns = [
    path('', views.index, name='index'),
]
