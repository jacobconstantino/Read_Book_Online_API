from djongo import models
from djongo.models.fields import EmbeddedField

# Create your models here.


class Name(models.Model):
    first_name = models.CharField(max_length=254)
    middle_name = models.CharField(null= True,blank = True,max_length=254)
    last_name = models.CharField(null= True,blank = True,max_length=254)
    
    class Meta:
        abstract = True
        
class Users(models.Model):
    _id = models.ObjectIdField()
    email = models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    name = models.EmbeddedField(
        model_container = Name
    )
    phone_number = models.CharField(max_length=255)
    country = models.CharField(max_length=20)
    is_user_verified = models.BooleanField(default=False)
    agent= models.CharField(max_length=255)
    date_of_birth = models.DateField()
    date_created = models.DateField(auto_now_add= True)    
    date_updated = models.DateField(auto_now=True)
    created_by = models.CharField(null = True,blank = True,max_length=100)
    updated_by = models.CharField(null = True,blank = True,max_length=100)