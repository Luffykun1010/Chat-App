from django.contrib.auth.models import User
from django.db import models
class Room(models.Model):
    name=models.CharField(max_length=300)
    slug=models.SlugField(unique=True)
    def __str__(self):
        return self.name
class Messages(models.Model):
    room=models.ForeignKey(Room,related_name='messages',on_delete=models.CASCADE)
    user=models.ForeignKey(User,related_name='messages',on_delete=models.CASCADE)
    content=models.TextField()
    sended_on=models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['sended_on']