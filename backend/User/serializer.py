from rest_framework import serializers
from .models import Users
from django.contrib.auth import authenticate
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['username' , 'password' , 'UserInputID' ,'UserOutputID' ]
        extra_kwargs = {'password': {'write_only': True}}
    #password hashing 
    def create(self , validated_data):
        password = validated_data.pop('password')
        user = Users(**validated_data)
        user.set_password(password)
        user.is_active = True #login authentication method to work in the login 
        user.save()
        return user 
    

class LoginSerializer(serializers.Serializer):

    username = serializers.CharField(max_length = 150)
    password = serializers.CharField(write_only = True)
    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if username and password :
            user = authenticate(request=self.context.get('request'),username = username , password = password)
            if not user  :
               raise serializers.ValidationError(f'Invalide username {username} or password {password} and user {user}')
        else:
            raise serializers.ValidationError('Invalide username and password')

        data['user'] = user
        return data
