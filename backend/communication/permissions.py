from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from .models import ApiKeys

class HasAPIKey(BasePermission):
    def has_permission(self, request, view):
        key = request.headers.get('Api-Key')
        if not key:
            return False
        try:
            return ApiKeys.objects.filter(key_hash=key)
        except:
            return AuthenticationFailed('Invalide APIkey')