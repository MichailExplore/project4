from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

_AVATAR_URL = 'https://res.cloudinary.com/mhmd/image/upload/v1564960395/avatar_usae7z.svg'


class User(AbstractUser):
    birthday = models.DateField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    avatar = models.CharField(max_length=100, default=_AVATAR_URL)

    def __str__(self):
        return '{} {} ({})'.format(self.first_name, self.last_name, self.email)

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date = models.DateField(auto_now_add=True)
    time = models.TimeField(auto_now_add=True)
    message = models.TextField()

    def __str__(self):
        return '{} ({})'.format(self.message, self.user.first_name)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    message = models.TextField()

    def __str__(self):
        str_ = 'Comment by {} on post of {}: {}'
        str_ = str_.format(self.user.first_name, self.post.user.first_name, self.message)
        return str_

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked')

    def __str__(self):
        return '{} liked post by {}: {}'.format(self.user.first_name, self.post.user.first_name,
                                                self.post.message)
