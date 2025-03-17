from zendesk import views
from django.urls import path

# URL patterns
urlpatterns = [
    path('', views.index, name='index'),
    path('save-data/', views.process_ticket_data, name='save-data')
]
