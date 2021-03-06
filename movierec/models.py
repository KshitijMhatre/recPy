from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver

from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import AddUser

from . import myconfig

client = RecombeeClient(myconfig.mov_db,myconfig.token)
bclient = RecombeeClient(myconfig.book_db,myconfig.btoken)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    u_id = models.AutoField(primary_key=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        prof=Profile.objects.create(user=instance)        
        try:
            client.send(AddUser(prof.u_id)) 
        except:
            pass
        try:            
            bclient.send(AddUser(prof.u_id)) 
        except:
            print("Using existing profile")

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

def update_profile(request, user_id):
    user = User.objects.get(pk=user_id)
    user.profile.bio = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit...'
    user.save()

class Ratings(models.Model):
    uid= models.IntegerField()
    imdb = models.CharField(max_length=30)
    rating = models.FloatField(default=0.0)
