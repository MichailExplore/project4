from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    context = {
        'user': request.user
    }
    return render(request, 'network/index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        context = {
            'message': 'You are alread logged in.'
        }
        return render(request, 'network/index.html', context)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        context = {
            'message': 'Oops! Invalid credentials for privacyinvader.com.'
        }
        return render(request, 'network/login.html', context)
    return render(request, 'network/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))

def register(request):
    if request.user.is_authenticated:
        context = {
            'message': 'You cannot register while logged into privacyinvader.com.'
        }
        return render(request, 'network/index.html', context)
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        first_name = request.POST['first-name']
        last_name = request.POST['last-name']

        if password != request.POST['confirmation']:
            context = {
                'message': 'Oops! Passwords do not match.'
            }
            return render(request, 'network/register.html', context)

        try:
            # helper function used when creating User object (hashing related)
            user = User.objects.create_user(username=email, password=password,
                                            first_name=first_name,
                                            last_name=last_name)
            user.save()
        except IntegrityError:
            context = {
                'message': 'Oops! That email already exists on privacyinvader.com.'
            }
            return render(request, 'network/register.html', context)
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'network/register.html')

@login_required
def get_posts(request):
    posts = Post.objects.all().values('message', 'date', 'time', 'likes',
                                      'dislikes', 'user__avatar', 'user',
                                      'user__first_name', 'user__last_name').order_by('-date', '-time')
    for post in posts:
        post['own_post'] = False
        if post['user'] == request.user.id:
            post['own_post'] = True
    posts = list(posts)
    return JsonResponse(posts, safe=False)

@login_required
def create_post(request):
    try:
        message = request.POST['post-input']
    except Exception:
        context = {
            'message': 'Oops! Could not post.'
        }
        return render('network/index.html', context)
    user = request.user
    post = Post(user=user, message=message)
    post.save()
    return JsonResponse(list(post), safe=False)
