# Imports
# - Django
from django.shortcuts import render

# - Rest Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

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
    return Response({'message': 'Debug', 'data': request.data}, status=status.HTTP_200_OK)
