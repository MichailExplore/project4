from . import views
from django.urls import path


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    ### path('api/adjust-emotion/<int:sentiment>/<int:post_id>', views.adjust_emotion)
]
