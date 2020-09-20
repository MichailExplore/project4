
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('api/create-post', views.create_post, name='create-post'),
    path('api/adjust-emotion/<int:sentiment>/<int:post_id>', views.adjust_emotion),
    path('api/get-posts/<str:filter_by>', views.get_posts),
    path('api/get-post/<int:post_id>', views.get_post),
    path('api/delete-post/<int:post_id>', views.delete_post),
    path('api/update-post/<int:post_id>', views.update_post)
]
