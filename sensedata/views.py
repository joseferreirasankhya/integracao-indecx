# Imports
# - Django
from django.shortcuts import render
# - Rest Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# - JSON
import json
# - Services
from sensedata.services.nps_service import NPSService

# Configuring NPS Service
nps_service = NPSService()

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
def debug_nps(request):
    '''
    Debug route for testing
    '''
    # If request data is provided
    if 'answer' in request.data:
        # Transform request data to Sense NPS API JSON format
        data = nps_service.transform_nps_data(request.data['answer'])
        # If data is provided
        if data:
            # Return response with data
            return Response({'message': 'Debug', 'data': data}, status=status.HTTP_200_OK)
        else:
            # Return response with error message
            return Response({'message': 'Wrong metric, please check the metric name'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        # Return response with error message
        return Response({'message': 'No data provided'}, status=status.HTTP_400_BAD_REQUEST)
