from rest_framework import serializers

from .models import Stories , StoryComment , StoryShare
from users_app.models import Users
from users_app.serializers import UserSerializers
from bson.objectid import ObjectId

class StoryCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryComment
        fields = '__all__'
    
class StoryShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoryShare
        fields = '__all__'

class StoriesSerializer(serializers.ModelSerializer):
    author = UserSerializers(many= True,required = False)
    co_author = UserSerializers(many= True,required = False)
    user_view_list = UserSerializers(many= True,required = False)
    users_like_list = UserSerializers(many= True,required = False)
    users_comment = StoryCommentSerializer(many= True,required = False)
    users_share = StoryShareSerializer(many= True,required = False)
    original_content = serializers.CharField(required=False)
    content = serializers.CharField(required=False)


    def create(self,validated_data):

        authors = validated_data.pop('author')
        co_authors = validated_data.pop('co_author')

        author_id = []
        co_author_id = []

        if authors is not None:
    
            for author in authors:   
                try:
                    users_id= Users.objects.get(_id = ObjectId(author['id']))       
                except Users.DoesNotExist:
                    raise serializers.ValidationError("Author/s ID not found")

                author_id.append(users_id)  

        if co_authors is not None:
    
            for co_author in co_authors:   
                try:
                    users_id= Users.objects.get(_id = ObjectId(co_author['id']))       
                except Users.DoesNotExist:
                    raise serializers.ValidationError("Co Author/s ID not found")

                co_author_id.append(users_id)  

        new_story = Stories.objects.create(**validated_data)

        for author in author_id: new_story.author.add(author) if author_id != []  else ""
        for co_author in co_author_id: new_story.co_author.add(co_author) if co_author_id != []  else ""

        new_story.save()
    
        return new_story

    def update(self,instance,validated_data):
    
        instance.story_cover = validated_data.get('story_cover', instance.story_cover)
        instance.type = validated_data.get('type', instance.type)
        instance.chapter = validated_data.get('chapter', instance.chapter)
        # instance.packages = validated_data.get('packages', instance.packages)
        instance.genre = validated_data.get('genre', instance.genre)
        instance.original_content =  instance.original_content
        instance.updated_content = validated_data.get('content', instance.updated_content)
        instance.title = validated_data.get('title', instance.title)
        instance.price = validated_data.get('price', instance.price)
        # instance.password = instance.password
        instance.status = validated_data.get('status', instance.status)
        instance.engagement = validated_data.get('engagement', instance.engagement)

    
        authors = validated_data.pop('author',None)
        co_authors = validated_data.pop('co_author',None)
        users_view_lists = validated_data.pop('users_view_list',None)
        users_like_lists = validated_data.pop('users_like_list',None)
        users_comments = validated_data.pop('users_comment',None)
        users_shares = validated_data.pop('users_share',None)

        if authors is not None:
        
            for author in authors:   
                try:
                    author_id= Users.objects.get(_id = ObjectId(author['id']))       
                except Users.DoesNotExist:
                    raise serializers.ValidationError("Author/s ID not found")

                instance.author.add(author_id)  

        if co_authors is not None:
    
            for co_author in co_authors:   
                try:
                    co_author_id= Users.objects.get(_id = ObjectId(co_author['id']))       
                except Users.DoesNotExist:
                    raise serializers.ValidationError("Co Author/s ID not found")

                instance.co_author.add(co_author_id)  

        if users_view_lists is not None:
        
            for user in users_view_lists:   
                try:
                    user_id= Users.objects.get(_id = ObjectId(user['id']))       
                except Users.DoesNotExist:
                    raise serializers.ValidationError("User/s view list  ID not found")

                instance.users_view_list.add(user_id)  
        
        if users_like_lists is not None:
            
            for user in users_like_lists:   
                try:
                    user_id= Users.objects.get(_id = ObjectId(user['id']))       
                except Users.DoesNotExist:
                    raise serializers.ValidationError("User/s like list  ID not found")

                instance.users_like_list.add(user_id)  

        if users_comments is not None:
                
            for comment in users_comments:   
                try:
                    comment_id= StoryComment.objects.get(_id = ObjectId(comment['id']))       
                except StoryComment.DoesNotExist:
                    raise serializers.ValidationError("User/s comment  ID not found")

                instance.users_comment.add(comment_id)  
     
        if users_shares is not None:
                
            for share in users_shares:   
                try:
                    share_id= StoryShare.objects.get(_id = ObjectId(share['id']))       
                except StoryShare.DoesNotExist:
                    raise serializers.ValidationError("User/s share list  ID not found")

                instance.users_share.share(share_id)  
        
        instance.save()

        return instance
    class Meta:
        model = Stories
        fields = '__all__'