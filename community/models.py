from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse

class Category(models.Model):
    """
    Forum categories to organize discussions into different topics.
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "categories"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('community:category_detail', kwargs={'slug': self.slug})

class Post(models.Model):
    """
    Forum posts that can be either regular posts or special submissions.
    """
    POST_TYPE_CHOICES = (
        ('discussion', 'Discussion (visible to all logged-in users)'),
        ('announcement', 'Announcement (important updates)'),
        ('submission', 'Submission (visible only to staff)'),
    )
    
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='discussion')
    is_pinned = models.BooleanField(default=False)
    is_locked = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    last_activity = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-is_pinned', '-last_activity']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('community:post_detail', kwargs={'pk': self.pk})

    def vote_score(self):
        """Calculate the total score based on upvotes and downvotes."""
        return self.votes.aggregate(score=models.Sum('value'))['score'] or 0

class Comment(models.Model):
    """
    Comments on forum posts, supporting nested discussions.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_comments')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

class Vote(models.Model):
    """
    Voting system for posts and comments.
    """
    VOTE_CHOICES = (
        (1, 'Upvote'),
        (-1, 'Downvote'),
    )
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='community_votes')
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f"{self.user.username} voted {self.value} on {self.post.title}"
