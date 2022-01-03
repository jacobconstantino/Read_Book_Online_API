from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.shortcuts import render
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_206_PARTIAL_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_205_RESET_CONTENT,HTTP_401_UNAUTHORIZED
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Users
# from .read_book_online.settings import EMAIL_HOST_USER as EmailSender
from django.shortcuts import get_list_or_404 ,get_object_or_404
from .serializers import UserSerializers
from bson.objectid import ObjectId
# Create your views here.
import jwt
import json

class Mailer():

    def SendEmailVerification(email,id):
      
        user = get_object_or_404(Users, _id=ObjectId(id))
        serializer = UserSerializers(user)

        email_template = 'EmailVerification.html'
        template = "email/"+ email_template
        name = json.loads(serializer.data['name'])

        data = {
            "id" : serializer.data['_id']
        }

        parse_token = jwt.encode(data,"secret",)

        message = get_template(template).render({'data':parse_token , 'first_name' : name['first_name']})
        

        mail = EmailMessage(
            subject="Email Verification",
            body=message,   
            from_email='no-reply@read-book-online.net',
            to=[email],
        )

        mail.content_subtype = "html" 
        mail.send() 

        return 'sent'

    def VerifyUser(self,token):

        parse_token = jwt.decode(token, algorithms='HS256', options={'verify_signature': False})

        user = get_object_or_404(Users, _id=ObjectId(parse_token['id']))

        data = {
            "is_user_verified" : True
        }
        
        serializer = UserSerializers(user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return render(self,'email/pop.html',{"message":"Verification Success"})