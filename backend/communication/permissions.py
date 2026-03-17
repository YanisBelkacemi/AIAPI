from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed
from .models import ApiKeys
from django.contrib.auth.hashers import check_password
#this here is used for Api check for our custom api model
class HasAPIKey(BasePermission):
    def has_permission(self, request, view):
        #gets the API key from the headers
        key = request.headers.get('Api-Key')
        if not key:
            return False
        try:
            #here we are checking for all the API keys to find if ours is valide
            
            for k in key:
                if ApiKeys.objects.filter(key_hash=check_password(key , k.key_hash)):
                    request.user = k.user
                    return True
        except:
            return AuthenticationFailed('Invalide APIkey')