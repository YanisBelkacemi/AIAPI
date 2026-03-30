
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializer import APIkeyserializer 
from User.models import Users
from .permissions import HasAPIKey
from .models import ApiKeys
import requests
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .throttles import QuotaLimitting
from .services.redis_client import Token_daily
# Create your views here.

class ApiKeyCreation(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self , request):
        APIkey = APIkeyserializer(data = request.data , context = {"request" : request})
        if APIkey.is_valid():
            APItoken = APIkey.save()
            Owner = Users.objects.get(id = APItoken.user.id)
            return Response({
                'Name' : APItoken.name,
                "key" : APItoken.raw_key,
                "Owner" : Owner.username,
                'UserInputID': Owner.UserInputID + ' (This is used for using the API key)'
            },  status=status.HTTP_201_CREATED,)
        return Response({"error" : APIkey.errors }, status=status.HTTP_400_BAD_REQUEST)
    
class ModelAccess(APIView):
    permission_classes=[HasAPIKey]
    throttle_classes = [QuotaLimitting]
    def post(self, request):
        #getting the API from the header
        API = request.headers.get("Api-Key")
        for Apimodel in ApiKeys.objects.filter( revoked = False , is_active = True):
            if check_password(API , Apimodel.key_hash):
                    #accessing the Middleware if the ApiKay is valid
                    url = 'http://127.0.0.1:8000/output'
                    try :
                        context = { "user" : request.user.username,
                                    "model" : request.data["model"] ,
                                    "prompt" : f"Summarize in 10 words:{request.data['prompt']}",
                                    "stream" : False,
                                    "options": {
                                                "num_predict": 30,
                                                "temperature": 0.4,
                                                "num_ctx": 1024
                                                }}
                        resp = requests.post(url ,
                                            json = context,
                                            proxies={"http": None, "https": None})
                        data =resp.json()
                        return Response({ 'Tokens' : Token_daily(API) ,'data' : data})
                    except requests.exceptions.RequestException:
                        return Response({'Exception' : 'Service unavailable'}, status=501)
        return Response({'error' : 'Your API key is not active' }, status=401)
        