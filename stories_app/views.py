from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_206_PARTIAL_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_205_RESET_CONTENT,HTTP_401_UNAUTHORIZED
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Stories
from django.shortcuts import get_list_or_404 ,get_object_or_404
from .serializers import StoriesSerializer
from bson.objectid import ObjectId
# Create your views here.
import jwt

class StoriesViewApi(APIView):
    
    def get(self, request):

        data = request.data['token'] 

        parse_token = jwt.decode(data, algorithms='HS256', options={'verify_signature': False})

        # if token_auth is True:
        stories = get_list_or_404(Stories)
        # users = User.objects.all()
        serializers = StoriesSerializer(stories, many=True)

        return Response(serializers.data, status=HTTP_200_OK)

        # else:
        #     return Response("No Access Token", status = HTTP_401_UNAUTHORIZED)

    def post(self, request):
        data = request.data['token'] 

        parse_token = jwt.decode(data, algorithms='HS256', options={'verify_signature': False})

        # token_auth = Helper.TokenAuthentication(data)

        # if token_auth is True:

        Users_data = {
            "story_cover": parse_token['story_cover'] , 
            "type": parse_token['type'],
            "genre": parse_token['genre'] if "genre" in parse_token.keys() else "",
            "chapter": parse_token['chapter'] if "chapter" in parse_token.keys() else "",
            "original_content": parse_token['original_content'] if "original_content" in parse_token.keys() else "",
            "title": parse_token['title'],
            "price": parse_token['price'] if "price" in parse_token.keys() else "",
            "status": parse_token['status'] if "status" in parse_token.keys() else "",
            "author": parse_token['author'] if "author" in parse_token.keys() else [],
            "co_author": parse_token['co_author'] if "co_author" in parse_token.keys() else [],
            "engagement": parse_token['engagement'] if "engagement" in parse_token.keys() else None,
        }

        serializer = StoriesSerializer(data=Users_data)

        if serializer.is_valid():
            serializer.save()
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
        stories = get_object_or_404(Stories, _id=ObjectId(parse_token['id']))
        serializer = StoriesSerializer(
            stories, data=parse_token, partial=True)

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
        stories = get_object_or_404(Stories, _id=ObjectId(parse_token['id']))
    
        serializer = StoriesSerializer(stories, data=parse_token)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)

        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)
        # else:
        #     return Response(token_auth.data, status = HTTP_401_UNAUTHORIZED)

class StoriesUpdateDeleteApiView(APIView):

    def get(self, request,token):

        parse_token = jwt.decode(token, algorithms='HS256', options={'verify_signature': False})


       
        # token_auth = Helper.TokenAuthentication(token)

        # if token_auth is True:
        stories = get_object_or_404(Stories,_id=ObjectId(parse_token['id']))
      
        serializer = StoriesSerializer(stories)
        return Response(serializer.data, status=HTTP_200_OK)
        # else:
        #     return Response(token_auth.data, status = HTTP_401_UNAUTHORIZED)


    def delete(self, request,token): 

        parse_token = jwt.decode(token, algorithms='HS256', options={'verify_signature': False})

        # token_auth = Helper.TokenAuthentication(token)

        # if token_auth is True:
        story = get_object_or_404(Stories, _id=ObjectId(parse_token['id']))
        story.delete()
        return Response({"message": "Successfully deleted"}, status=HTTP_204_NO_CONTENT)
        # else:
        #     return Response(token_auth.data, status = HTTP_401_UNAUTHORIZED)

