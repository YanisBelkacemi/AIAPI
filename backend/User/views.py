from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny , IsAuthenticated

#these here are used to csrf validation
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
#serializers
from .serializer import UserSerializer , LoginSerializer
from rest_framework.authtoken.models import Token
#usual
from django.contrib.auth import authenticate, login as loginf , logout
from .models import Users
from rest_framework.response import Response
from rest_framework.views import APIView

#csrf token
@method_decorator(csrf_exempt , name='dispatch')
class Register(APIView):
    authentication_classes = [TokenAuthentication]  # no SessionAuthentication
    permission_classes = [AllowAny]
    def post(self , request):
        #getting the data from our request
        serializer = UserSerializer(data = request.data)
        # Create new user
        if serializer.is_valid():
            serializer.save()
            return Response({'response' : 'The user has been successfully created, check your database'})
        else:
            return Response({'response' : str(serializer.errors)})
        
#csrf for login api
@method_decorator(csrf_exempt , name='dispatch')
class login_view(APIView):
    #these here are used to bypass crsf tokens
    authentication_classes = [TokenAuthentication]  # no SessionAuthentication
    permission_classes = [AllowAny]
    def post(self , request):
        serializer = LoginSerializer(data= request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # token creation
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'username': user.username
            })
        return Response(serializer.errors, status=400)
@method_decorator(csrf_exempt , name='dispatch')    
class logout_view(APIView):
    #these here are used to bypass crsf tokens
    authentication_classes = [TokenAuthentication]  # no SessionAuthentication
    permission_classes = [IsAuthenticated] #IsAuthenticated is used here to ensure that a user is connected 
    
    def post(self , request):
        request.user.auth_token.delete()
        return Response({
            'response' : 'user successfully disconnected'
        })

