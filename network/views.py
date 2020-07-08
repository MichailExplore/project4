from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


def index(request):
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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        context = {
            'message': 'Oops! Invalid credentials.'
        }
        return render(request, 'network/login.html', context)
    return render(request, 'network/login.html')

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if password != request.POST['confirmation']:
            context = {
                'message': 'Oops! Passwords do not match.'
            }
            return render(request, 'network/register.html', context)

        try:
            # helper function used when creating User object (hashing related)
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            context = {
                'message': 'Oops! That username already exists.'
            }
            return render(request, 'network/register.html', context)
        login(request, user)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'network/register.html')

@login_required
def update_password(request):
    print('Mio')
    # user = request.user
    # user.set_password('admin')
    # user.save()
    # login(request, user)
    return HttpResponseRedirect(reverse('index'))