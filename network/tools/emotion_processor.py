from ..models import Emotion


class EmotionProcessor:

    @classmethod
    def add(cls, posts, request):
        """Add emotions information to posts."""
        posts = cls.emotion_count(posts, request, 1)
        posts = cls.emotion_count(posts, request, 2)
        return posts

    @classmethod
    def emotion_count(cls, posts, request, choice):
        """Add count of emotion to posts."""
        emotions = Emotion.objects.all().values().filter(sentiment=choice)
        for post in posts:
            emotions_ = emotions.filter(post_id=post['id'])
            if choice == 1:
                post['likes'] = len(emotions_)
                post['have_liked'] = cls.have_reacted(emotions_, request)
            else:
                post['dislikes'] = len(emotions_)
                post['have_disliked'] = cls.have_reacted(emotions_, request)
        return posts

    @staticmethod
    def have_reacted(emotions_, request) -> bool:
        """Check if user has reacted to post with emotion in question."""
        l = list(emotions_.values('user_id'))
        l = [entry['user_id'] for entry in l]
        if request.user.id in l:
            return True
        return False
