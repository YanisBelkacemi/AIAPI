from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["get"])
def inputUser(res):
    Inp = {'model' : 'gamma3' , 'prompt' : "this is an access from a django simple api ", 'stream' : False}
    return Response(Inp)


