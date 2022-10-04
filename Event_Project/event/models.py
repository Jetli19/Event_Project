from django.db import models
from django.contrib.auth.models import AbstractUser, User


class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True) # pomoze nam identifikovat kto vytvoril roomku
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants = models.ManyToManyField(
    #       User, related_name='participants', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', '-updated'] # zoradi od najnovsej nahore nie od najstarsich

    def __str__(self):
        return self.name
'''
    def messages_count(self):
        room_messages = self.message_set.all()
        return room_messages.count()

    def last_message_time(self):
        room_message = self.message_set.all()[0]
        return room_message.updated
'''

'''
class Message(models.Model):
    body = models.TextField(null=False, blank=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created', '-updated'] # - nam zoradi opacne aod najnovsieho nie od najstarsieho

    def __str__(self):
        return self.body[0:50]
'''