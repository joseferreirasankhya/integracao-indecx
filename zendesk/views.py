from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from zendesk.services.csat_service import CSATService
from dotenv import load_dotenv
import os
import logging

# URLs
@api_view(['GET'])
def index(request):
    """Tests if API is responding correctly"""
    return Response({'message': 'Hello from Zendesk!'})
