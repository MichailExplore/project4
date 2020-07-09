from django.contrib.auth.models import AbstractUser
from django.db import models

import os


class User(AbstractUser):
    """A model for users."""
    birthday = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.CharField(max_length=100, default='https://res.cloudinary.com/mhmd/image/upload/v1564960395/avatar_usae7z.svg')

    def __str__(self):
        return '{} (id: {})'.format(self.first_name, self.id)

class Post(models.Model):
    """A model that keeps track of posts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField()
    likes = models.IntegerField(default=0)

    def __str__(self):
        return '{}: {}'.format(self.user.username, self.message)
