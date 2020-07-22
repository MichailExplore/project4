from .comment_processor import CommentProcessor
from .emotion_processor import EmotionProcessor
from ..models import Post

class PostProcessor:

    _VALUES = [
        'id',
        'user',
        'user__first_name',
        'user__last_name',
        'user__avatar',
        'message',
        'date',
        'time'
    ]

    _ORDER_BY = [
        '-date',
        '-time'
    ]

    @classmethod
    def process(cls, request, filter_by) -> list:
        """Method that processes Post."""
        posts = Post.objects.all().values(*cls._VALUES)
        posts = cls.filter_posts(posts, request, filter_by)
        posts = cls.order_posts(posts)
        posts = cls.edit_time(posts)
        posts = cls.add_own_post_status(posts, request)
        posts = EmotionProcessor.add(posts, request)
        return list(posts)

    @staticmethod
    def add_own_post_status(posts, request):
        """Add boolean field that indicates whether current user made post."""
        for post in posts:
            post['own_post'] = False
            if post['user'] == request.user.id:
                post['own_post'] = True
        return posts

    @staticmethod
    def edit_time(posts):
        """Drop seconds and milliseconds from time."""
        for post in posts:
            post['time'] = post['time'].strftime('%H:%M')
        return posts

    @staticmethod
    def filter_posts(posts, request, filter_by):
        """Filter posts according to argument."""
        if filter_by == 'all':
            return posts
        if filter_by == 'following':
            return posts
        if filter_by == 'user':
            return posts.filter(user=request.user.id)
        return posts.filter(pk=filter_by)

    @classmethod
    def order_posts(cls, posts):
        """Method that orders posts."""
        posts = posts.order_by(*cls._ORDER_BY)
        return posts
