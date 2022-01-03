from djongo import models
from users_app.models import Users
# Create your models here.



class StoryComment(models.Model):
    _id = models.ObjectIdField()
    user = models.OneToOneField(
        to = Users,
        on_delete= models.CASCADE,
    )
    original_content = models.TextField()
    updated_content = models.TextField()
    agent = models.TextField()
    date_created = models.DateField(auto_now_add= True)    
    date_updated = models.DateField(auto_now=True)

class StoryShare(models.Model):
    _id = models.ObjectIdField()
    user = models.OneToOneField(
        to = Users,
        on_delete= models.CASCADE,
    )
    original_caption = models.TextField()
    updated_caption = models.TextField()
    agent = models.TextField()
    date_created = models.DateField(auto_now_add= True)    
    date_updated = models.DateField(auto_now=True)

class StoryEngagement(models.Model):
    likes_count = models.BigIntegerField(default=0)
    shares_count = models.BigIntegerField(default=0)
    comments_count = models.BigIntegerField(default=0)
    views_count = models.BigIntegerField(default=0)
    
    class Meta:
        abstract = True
        
class Stories(models.Model):
    _id = models.ObjectIdField()
    story_cover = models.CharField(max_length=255)
    type = models.CharField(max_length=255)
    genre = models.CharField(max_length=255)
    chapter = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    original_content = models.TextField()
    updated_content = models.TextField(null=True,blank=True)
    price = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    author = models.ArrayReferenceField(
        to = Users,
        on_delete= models.CASCADE,
        related_name="author",
    )
    co_author =  models.ArrayReferenceField(
        to = Users,
        on_delete= models.CASCADE,
        related_name="co_author",
        null= True
    )

    users_view_list = models.ArrayReferenceField(
        to = Users,
        on_delete= models.CASCADE,
        related_name="user_view_list",
        null= True
    )

    users_like_list = models.ArrayReferenceField(
        to = Users,
        on_delete= models.CASCADE,
        related_name="users_like_list",
        null= True
    )
    users_comment = models.ArrayReferenceField(
        to = StoryComment,
        on_delete= models.CASCADE,
        null= True
    )
    users_share = models.ArrayReferenceField(
        to = StoryShare,
        on_delete= models.CASCADE,
        null= True
    )

    engagement = models.EmbeddedField(
        model_container = StoryEngagement,
        null = True
    )
    date_created = models.DateField(auto_now_add= True)    
    date_updated = models.DateField(auto_now=True)
    created_by = models.CharField(null = True,blank = True,max_length=100)
    updated_by = models.CharField(null = True,blank = True,max_length=100)