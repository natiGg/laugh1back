from datetime import date
from email.policy import default
from django.db import models
from django.utils.timezone import timezone
from authentication.models import User
import uuid

# Create your models here.



class Roast(models.Model):
   
    STAGE_CHOICES = (
        ('special', 'special'),
        ('Far', 'Far'),
        ('Very close', 'close'),
        ('to be roasted', 'tobe'),
    )  
    stage = models.CharField(max_length=50, choices=STAGE_CHOICES)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    is_special=models.BooleanField(default=False)

 
class UserProfile(models.Model):

    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False,blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile',unique=True)
    name = models.CharField(max_length=50,unique=False,blank=True)
    phone_number = models.CharField(max_length=50, unique=False, null=False, blank=True)
    profile_pic = models.ImageField(null=True,blank=True,upload_to="profiles/")
    bod =models.DateField(null=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,blank=True)
    LEVEL_CHOICES = (
        ('comedian', 'comedian'),
        ('pro', 'pro'),
        ('amatuer', 'amatuer'),
        ('roaster', 'roaster'),
        ('spectator', 'spectator'),
    )
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES,default='spectator')
    bio = models.CharField(max_length=250,unique=False,default="bio")
    class Meta:
        '''
        to set table name in database
        '''
        db_table = "profile"
        
class Reaction(models.Model):
    
    REACTION_CHOICES = (
        ('haha', 'Funny'),
        ('ohhh', 'amazed'),
        ('nahh', 'Not Funny'),

    )
    reaction = models.CharField(max_length=50, choices=REACTION_CHOICES)

class Comment(models.Model):
    commenter = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    comment = models.TextField(blank=False)
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    reaction = models.ForeignKey(Reaction,on_delete=models.CASCADE,related_name='commentreact')
   
class Joke(models.Model):

    caption = models.TextField(blank=False)
    photo = models.ImageField(blank=True,upload_to='media/jokes_photo/')
    reaction = models.ManyToManyField(Reaction,related_name="reacted")  
    date_posted = models.DateField(auto_now_add=True)
    time_posted = models.TimeField(auto_now_add=True)
    posted_by = models.ForeignKey(to=User,on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment,on_delete=models.CASCADE,null=True)
    stage = models.OneToOneField(Roast,on_delete=models.CASCADE,null=True)
