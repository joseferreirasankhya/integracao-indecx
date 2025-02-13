from django.contrib.auth.models import AnonymousUser
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings

class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self, request):
        api_key = request.headers.get('Authorization')

        if api_key is None:
            raise AuthenticationFailed('No API key provided.')

        if api_key != f'Bearer {settings.API_KEY}':
            raise AuthenticationFailed('Invalid API key.')

        return AnonymousUser(), None  # Retorna um usuário válido
