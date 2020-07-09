from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    """A model for users."""
    birthday = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.CharField(max_length=100, default='https://res.cloudinary.com/mhmd/image/upload/v1564960395/avatar_usae7z.svg')
    # TODO: replace link with something from environment.

    def __str__(self):
        return '{} (id: {})'.format(self.first_name, self.id)

class Post(models.Model):
    """A model that keeps track of posts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='posts')
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    message = models.TextField()

    def __str__(self):
        return '{}: {}'.format(self.user.first_name, self.message)

class Comment(models.Model):
    """A model for comments."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    message = models.TextField()

    def __str__(self):
        return 'Comment by {} on post of {}: {}'.format(self.user.first_name,
                                                        self.post.user.first_name,
                                                        self.message)
