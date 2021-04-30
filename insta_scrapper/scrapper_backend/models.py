from django.db import models

class InstagramUser(models.Model):
    followers = models.IntegerField()
    followings = models.IntegerField()
    full_name = models.CharField(max_length=128)
    username = models.CharField(max_length=128,unique=True,primary_key=True)
    hash_tag = models.CharField(max_length=128)
    is_private = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
