from rest_framework.response import Response
from rest_framework.decorators import api_view
from zendesk.services.csat_service import CSATService

csat = CSATService()

# URLs
@api_view(['GET'])
def index(request):
    """Tests if API is responding correctly"""
    return Response({'message': 'Hello from Zendesk!'})

@api_view(['POST'])
def process_ticket_data(request):
    """Receive ticket data body from webhook"""
    response = csat.save_data(request)
    return Response({'status': 'ok', 'data': {"inserted_id": str(response.inserted_id)}})

@api_view(['POST'])
def debug_ticket_data(request):
    """Receive ticket data body from webhook"""
    return Response({'status': 'ok', 'data': request.data})
