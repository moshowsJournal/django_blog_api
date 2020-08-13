from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.api.serializers import RegistrationSerializer,LoginSerializer, TokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from itertools import chain


@api_view(['POST'])
def registration_view(request):
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        data = {
            'status':True,
            'code':201,
            'message':'Success! Account created.',
            'data': {
                'user':user.email,
                'token' : Token.objects.get(user=user).key
            }
        }
        return Response(data,status=201)
    else:
        errors = []
        for key,error_message in serializer.errors.items():
            errors.append(error_message[0])
        data = {
            'status':False,
            'message':errors[0],
            'code':400
        }
        return Response(data,status=400)
    
@api_view(['POST'])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validate(request.data)
        token = Token.objects.get(user=user).key
        data = {
            'status':False,
            'data':{
                'token': token
            },
            'message':'Login was successful'
        }
        return Response(data,200)
    errors = []
    for key,error_msg in serializer.errors.items():
        errors.append(error_msg[0])
    data = {
        'status' : False,
        'message' : errors[0]
    }
    return Response(data,400)