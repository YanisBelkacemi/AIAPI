from rest_framework import serializers
from .models import ApiKeys
import secrets
class APIkeyserializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, allow_blank=True)
    class Meta():
        model = ApiKeys
        fields = ["name"]

    def create(self , data):
        user = self.context['request'].user
        key = secrets.token_hex(32)
        key_prefix = data.get('name')
        name =  user.username + ' ' + data.get('name')
        user_id = user
        
        apikey = ApiKeys.objects.create(
            key_hash = key,
            key_prefix = key_prefix,
            name = name,
            user = user_id,
            revoked = False,
        )
        return apikey
    
class APIKeyValidation(serializers.ModelSerializer):
    class Meta():
        model = ApiKeys
        fields = ['key_hash']
