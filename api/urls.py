from . import views
from django.urls import path


urlpatterns = [
    path('create-post', views.create_post, name='create-post'),
    path('get-posts', views.get_posts),
    path('get-post/<post_pk>', views.get_post),
    path('delete-post/<post_pk>', views.delete_post),
    path('update-post/<post_pk>', views.update_post),
    path('like/<post_pk>', views.like)
]
