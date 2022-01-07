from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey('Topic', on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    #participants =
    updated = models.DateTimeField(auto_now=True) #Take a snapshot everytime
    created = models.DateTimeField(auto_now_add=True) #This time once is created never changes

    
    class Meta:
        ''''
        Order the list of rooms
        De arriba a abajo por el -, sino se ordenaria desde abajo
        '''
        ordering = ['-updated', '-created']

    def __str__(self):
        """only returns room name"""
        return self.name

class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    '''
    FK from Room
    on_delete = models.CASCADE because if some room is deleted, all the messages must be deleted
    '''
    room = models.ForeignKey(Room, on_delete=models.CASCADE) #Many to One relationship (one room multiple messages)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True) #Take a snapshot everytime
    created = models.DateTimeField(auto_now_add=True) #This time once is created never changes

    def __str__(self):
        """"""
        return self.body[0:50]

