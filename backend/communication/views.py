from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from . import utils
from rest_framework.permissions import IsAuthenticated , AllowAny
from .serializer import APIkeyserializer , APIKeyValidation
from User.models import Users
from .permissions import HasAPIKey
from .models import ApiKeys
import requests
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
                "key" : APItoken.key_hash,
                #'owner' : Users.objects.get(id = APItoken.user_id.
                "Owner" : Owner.username,
                'UserInputID': Owner.UserInputID + ' (This is used for using the API key)'

            })
        return Response({"error" : APIkey.error, 'name' : APIkey.data})
    
class ModelAccess(APIView):
    permission_classes=[HasAPIKey]
    def post(self, request):
        API = request.headers.get("Api-Key")
        Apimodel = ApiKeys.objects.filter(key_hash = API).first()
        if Apimodel:
            url = 'http://127.0.0.1:8000/output'
            resp = requests.post(url ,
                                 json = request.data,
                                  proxies={"http": None, "https": None} )
            data =resp.json()
            return Response(data)
        return Response({'response' : str(API)})
        