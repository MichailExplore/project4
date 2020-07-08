from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return '{}, {} (id: {})'.format(self.username, self.email, self.id)
