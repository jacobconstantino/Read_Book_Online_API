from django.http import request
from django.shortcuts import render
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_206_PARTIAL_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_205_RESET_CONTENT,HTTP_401_UNAUTHORIZED
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Users
from django.shortcuts import get_list_or_404 ,get_object_or_404
from .serializers import UserSerializers
from bson.objectid import ObjectId
from .mailer_views import Mailer
# Create your views here.
import jwt
from rest_framework.decorators import api_view

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

@api_view(['GET'])

def RenderHtml(request):
    return render(request,'sample.html')

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html" 

class UserViewApi(APIView):

    def get(self, request):

        data = request.data['token'] 

        parse_token = jwt.decode(data, algorithms='HS256', options={'verify_signature': False})

        # if token_auth is True:
        users = get_list_or_404(Users)
        # users = User.objects.all()
        serializers = UserSerializers(users, many=True)

        return Response(serializers.data, status=HTTP_200_OK)

        # else:
        #     return Response("No Access Token", status = HTTP_401_UNAUTHORIZED)

    def post(self, request):
        data = request.data['token'] 

        parse_token = jwt.decode(data, algorithms='HS256', options={'verify_signature': False})

        # token_auth = Helper.TokenAuthentication(data)

        # if token_auth is True:

        Users_data = {
            "email": parse_token['email'],
            "password": parse_token['password'], 
            "name": parse_token['name'],
            "is_user_verified": False,
            "phone_number": parse_token['phone_number'] if "phone_number" in parse_token.keys() else "",
            "country": parse_token['country'] if "country" in parse_token.keys() else "",
            "agent": parse_token['agent'] if "agent" in parse_token.keys() else "",
            "date_of_birth": parse_token['date_of_birth'] 
        }
     
        serializer = UserSerializers(data=Users_data)

        if serializer.is_valid():
            serializer.save()

            try:
                email = Mailer.SendEmailVerification(serializer.data['email'],serializer.data['_id'])
            except:
                raise Exception("Email verification failed to send")

            return Response(serializer.data, status=HTTP_201_CREATED)
            
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(token_auth.data, status = HTTP_401_UNAUTHORIZED)

    def patch(self, request):
        
        data = request.data['token'] 

        parse_token = jwt.decode(data, algorithms='HS256', options={'verify_signature': False})

        # token_auth = Helper.TokenAuthentication(data)

        # if token_auth is True:
            # parse_token['updated_by'] = session_name(request)
        users = get_object_or_404(Users, _id=ObjectId(parse_token['id']))
        serializer = UserSerializers(
            users, data=parse_token, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_206_PARTIAL_CONTENT)

        return Response(status=HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(token_auth.data, status = HTTP_401_UNAUTHORIZED)
    
    def put(self, request):
        data = request.data['token'] 

        parse_token = jwt.decode(data, algorithms='HS256', options={'verify_signature': False})

        # token_auth = Helper.TokenAuthentication(data)

        # if token_auth is True:
            # parse_token['updated_by'] = session_name(request)
        users = get_object_or_404(Users, _id=ObjectId(parse_token['id']))
        serializer = UserSerializers(users, data=parse_token)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(token_auth.data, status = HTTP_401_UNAUTHORIZED)

class UserUpdateDeleteApiView(APIView):

    def get(self, request,token):

        parse_token = jwt.decode(token, algorithms='HS256', options={'verify_signature': False})

        # token_auth = Helper.TokenAuthentication(token)

        # if token_auth is True:
        users = get_object_or_404(Users,_id=ObjectId(parse_token['id']))
        serializer = UserSerializers(users)
        return Response(serializer.data, status=HTTP_200_OK)
        # else:
        #     return Response(token_auth.data, status = HTTP_401_UNAUTHORIZED)


    def delete(self, request,token): 

        parse_token = jwt.decode(token, algorithms='HS256', options={'verify_signature': False})

        # token_auth = Helper.TokenAuthentication(token)

        # if token_auth is True:
        users = get_object_or_404(Users, _id=ObjectId(parse_token['id']))
        users.delete()
        return Response({"message": "Successfully deleted"}, status=HTTP_204_NO_CONTENT)
        # else:
        #     return Response(token_auth.data, status = HTTP_401_UNAUTHORIZED)

