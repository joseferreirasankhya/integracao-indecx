from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes
from sensedata.authentication import APIKeyAuthentication
from sensedata.services.nps_service import NPSService
from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

nps_service = NPSService(
    api_url=os.getenv('SENSE_NPS_API_URL'),
    api_key=f"{os.getenv('SENSE_NPS_API_KEY')}="
)

# URLs
@api_view(['GET'])
def index(request):
    """Tests if API is responding correctly"""
    return Response({'message': 'Hello, World!'})

@api_view(['POST'])
def debug_nps(request):
    """Debug endpoint for NPS data transformation"""

    if not request.data:
        logger.warning("No data provided in the request.")
        return Response(
            {'message': 'No data provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(request.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def process_nps(request):
    """Endpoint para processar dados do NPS"""
    if not request.data:
        return Response(
            {'message': 'No data provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        answer_data = request.data.get('answers') or request.data.get('answer')

        # Garante que o dado é um dicionário válido
        if not answer_data:
            return Response(
                {'message': 'Invalid data format'},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = nps_service.process_nps_data(answer_data)
        return Response(result)
    except ValueError as e:
        return Response(
            {'message': str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        logger.error("Error processing NPS data: %s", str(e))
        return Response(
            {'message': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
