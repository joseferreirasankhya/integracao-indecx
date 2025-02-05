from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from sensedata.services.nps_service import NPSService
from django.conf import settings

nps_service = NPSService(
    # api_url=settings.SENSE_API_URL,
    # api_key=settings.SENSE_API_KEY
)

@api_view(['GET'])
def index(request):
    """Tests if API is responding correctly"""
    return Response({'message': 'Hello, World!'})

@api_view(['POST'])
def debug_nps(request):
    """Debug endpoint for NPS data transformation"""
    if not request.data:
        return Response(
            {'message': 'No data provided'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    transformed_data = nps_service.process_nps_data(request.data.get('answer'))
    if not transformed_data:
        return Response(
            {'message': 'Invalid data format'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(transformed_data, status=status.HTTP_200_OK)


@api_view(['POST'])
def process_nps(request):
    """Endpoint para processar dados do NPS"""
    if not request.data:
        return Response(
            {'message': 'No data provided'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        result = nps_service.process_nps_data(request.data.get('answer'))
        return Response(result)
    except ValueError as e:
        return Response(
            {'message': str(e)}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            {'message': str(e)}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
