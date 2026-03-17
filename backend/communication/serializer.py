from rest_framework import serializers
from .models import ApiKeys
import secrets
from django.contrib.auth.hashers import make_password
class APIkeyserializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, allow_blank=True)
    class Meta():
        model = ApiKeys
        fields = ["name"]
    def create(self , data):
        user = self.context['request'].user
        key = secrets.token_hex(32)
        key_hash = make_password(key)
        key_prefix = key[:8]
        name =  user.username + ' ' + data.get('name')
        user_id = user
        is_active = True
        
        apikey = ApiKeys.objects.create(
            key_hash = key_hash,
            key_prefix = key_prefix,
            name = name,
            user = user_id,
            revoked = False,
            is_active = True
        )
        apikey.raw_key = key
        return apikey
    
class APIKeyValidation(serializers.ModelSerializer):
    class Meta():
        model = ApiKeys
        fields = ['key_hash']
