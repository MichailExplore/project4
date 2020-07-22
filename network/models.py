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
        return '{} {}'.format(self.first_name, self.last_name)

class Post(models.Model):
    """A model that keeps track of posts."""
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='posts')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return '{} ({})'.format(self.message, self.user.first_name)

class Comment(models.Model):
    """A model for comments."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    message = models.TextField()

    def __str__(self):
        str_ = 'Comment by {} on post of {}: {}'
        str_ = str_.format(self.user.first_name, self.post.user.first_name,
                           self.message)
        return str_

class Emotion(models.Model):
    """A model for likes and dislikes."""

    class Sentiment(models.IntegerChoices):
        Like = 1
        Dislike = 2

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sentiment = models.IntegerField(choices=Sentiment.choices)

    def __str__(self):
        return '{} had emotional response to post: "{}"'.format(self.user,
                                                                self.post)
