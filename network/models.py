from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """A model for users."""
    def __str__(self):
        return '{}, {} (id: {})'.format(self.username, self.email, self.id)

class Post(models.Model):
    """A model that keeps track of posts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField()
    message = models.TextField()
    likes = models.IntegerField(default=0)
