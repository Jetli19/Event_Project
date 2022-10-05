from django.db import models
from django.contrib.auth.models import AbstractUser, User


class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # participants = models.ManyToManyField(
    #     User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

    # def messages_count(self):
    #     room_messages = self.message_set.all()
    #     return room_messages.count()
    #
    # def last_message_time(self):
    #     room_message = self.message_set.all()[0]
    #     return room_message.updated


# class Message(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     room = models.ForeignKey(Room, on_delete=models.CASCADE)
#     body = models.TextField(null=False, blank=False)
#     file = models.TextField(null=True)  # file atribute in model
#     updated = models.DateTimeField(auto_now=True)
#     created = models.DateTimeField(auto_now_add=True)
#
#     class Meta:
#         ordering = ['-updated', '-created']
#
#     def __str__(self):
#         return self.body[0:50]
