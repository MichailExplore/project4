from django.contrib import admin
from .models import User, Post, Comment, Emotion


# Register your models here.
admin.site.register(User)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Emotion)
