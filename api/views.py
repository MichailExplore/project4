from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from network.models import Like, Post, User


@login_required
def create_post(request):
    message = request.POST['message']
    Post.objects.create(user=request.user, message=message)
    return HttpResponse('ok')

@login_required
def get_posts(request):
    posts = Post.objects.all()
    posts = posts.order_by(*['-date', '-time'])
    posts = posts.values(*['pk', 'user', 'user__first_name', 'user__last_name', 'user__avatar',
                           'message', 'date', 'time'])

    for post in posts:
        post['time'] = post['time'].strftime('%H:%M')

        post['own_post'] = False
        if post['user'] == request.user.id:
            post['own_post'] = True

        likes = Like.objects.all()
        likes = likes.filter(post_id=post['pk'])
        post['likes'] = len(likes)

        post['have_liked'] = False
        likes = likes.values(*['user_id'])
        likes = list(likes)
        for user in likes:
            if user['user_id'] == request.user.id:
                post['have_liked'] = True

    posts = list(posts)

    p = Paginator(posts, 5)
    # page = request.GET.get('page')
    posts_ = p.page(4)
    posts_ = list(posts_)
    posts_ = sorted(posts_, key = lambda i: (i['date'], i['time']))

    return JsonResponse(posts_, safe=False)

@login_required
def get_post(request, post_pk):
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist:
        return Http404('Trying to get post which does not exist.')
    message = {
        'message': post.message,
        'pk': post_pk
        }
    return JsonResponse(message, safe=False)

@login_required
def delete_post(request, post_pk):
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist:
        return HttpResponseRedirect(reverse('index'))
    if post.user_id != request.user.id:
        return HttpResponseRedirect(reverse('index'))
    post.delete()
    return HttpResponse('OK')

@login_required
def update_post(request, post_pk):
    if not request.method == 'POST':
        return HttpResponseRedirect(reverse('index'))
    message = request.POST['message']
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist:
        return Http404('Trying to amend post which does not exist.')
    if post.user_id != request.user.id:
        return HttpResponseRedirect(reverse('index'))
    post.message = message
    post.save()

    message = {'message': message}
    return JsonResponse(message, safe=False)

@login_required
def like(request, post_pk):
    try:
        post = Post.objects.get(pk=post_pk)
    except Post.DoesNotExist:
        return Http404('Trying to amend likes of post which does not exist.')
    likes = Like.objects.all()
    likes = likes.filter(post_id=post_pk)
    likes = likes.values(*['user_id'])
    likes = list(likes)

    users = [entry['user_id'] for entry in likes]
    if request.user.id not in users:
        Like.objects.create(user=request.user, post=post)
        likes = {'have_liked': True}
    else:
        Like.objects.filter(user=request.user, post=post).delete()
        likes = {'have_liked': False}
    likes['likes'] = len(Like.objects.all().filter(post_id=post_pk))
    return JsonResponse(likes, safe=False)
