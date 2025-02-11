# Create your models here.
from django.db import models
from django.conf import settings
from django.utils import timezone

class Post(models.Model):
    POST_TYPE_CHOICES = (
        ('post', 'Post (visible to all logged-in users)'),
        ('submission', 'Submission (visible only to staff)'),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts'
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    type = models.CharField(
        max_length=20, choices=POST_TYPE_CHOICES, default='post'
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def vote_score(self):
        # Calculate the sum of all votes for this post
        return sum(vote.value for vote in self.votes.all())

    def __str__(self):
        return self.title


class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Upvote'),
        (-1, 'Downvote'),
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='votes'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} voted {self.value} on {self.post.title}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
