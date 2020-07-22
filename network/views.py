from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Post, User, Emotion
from .tools import PostProcessor


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    context = {
        'user': request.user,
        'posts': PostProcessor.process(request, 'all')
    }
    return render(request, 'network/index.html', context)

def login_view(request):
    if request.user.is_authenticated:
        context = {
            'message': 'You are already logged in.'
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

@login_required
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
def create_post(request):
    message = request.POST['message']
    Post.objects.create(user=request.user, message=message)
    return HttpResponseRedirect(reverse('index'))

@login_required
def adjust_emotion(request, sentiment, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return Http404('Trying to amend emotion of post which does not exist.')
    emotions = Emotion.objects.all().filter(sentiment=sentiment, post=post_id).values('user')
    l = [entry['user'] for entry in list(emotions)]
    post = Post.objects.get(pk=post_id)
    if request.user.id not in l:
        Emotion.objects.create(user=request.user, sentiment=sentiment, post=post)
    else:
        Emotion.objects.filter(user=request.user, sentiment=sentiment, post=post).delete()
    return JsonResponse(list(PostProcessor.process(request, post_id)), safe=False)
