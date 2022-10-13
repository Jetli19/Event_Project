from django.db import models
from django.contrib.auth.models import AbstractUser, User
from datetime import *


class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    start_event = models.DateField(null=True, blank=True)
    end_event = models.DateField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name

    def comments_count(self):
        event_comments = self.comment_set.all()
        return event_comments.count()

    def last_comment_time(self):
        event_comments = self.comment_set.all()[0]
        return event_comments.updated


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    body = models.TextField(null=False, blank=False)
    file = models.TextField(null=True)  # file atribute in model
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]
