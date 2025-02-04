# Imports
# - Django
from django.shortcuts import render
# - Rest Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# - Sensedata
from sensedata.utils.nps import NPSData
# - JSON
import json

# Views

# - Index
@api_view(['GET'])
def index(request):
    '''
    Tests if API is responding correctly
    '''
    return Response({'message': 'Hello, World!'}, status=status.HTTP_200_OK)

# - Debug
@api_view(['POST'])
def debug(request):
    '''
    Debug route for testing
    '''
    # Transform request data to Python dictionary
    if request.data:
        return Response({'message': 'Debug', 'data': request.data}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'No data provided'}, status=status.HTTP_400_BAD_REQUEST)
