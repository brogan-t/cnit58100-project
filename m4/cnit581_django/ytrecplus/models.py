from django.db import models

# Create your models here.

class Account(models.Model):
    username = models.CharField(max_length=20, help_text="Enter a username")
    passphrase = models.CharField(max_length=20, help_text="Enter a passphrase")
    
class Video(models.Model):
    thumbnail = models.IntegerField()
    title = models.CharField(max_length=128, help_text="Enter the video title")
    description = models.CharField(max_length=8000, help_text="Enter a brief description of the video")
    channel = models.CharField(max_length=64, help_text="Enter a channel identifier")
    genre = models.CharField(max_length=30, help_text="Enter a genre identifier")
    
class Comment(models.Model):
    video = models.IntegerField()
    name = models.CharField(max_length=64, help_text="Enter user identifier")
    date = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=500, help_text="Enter a brief comment for the video")