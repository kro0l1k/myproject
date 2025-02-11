from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import UserMessage
from django.contrib.auth.decorators import login_required
from community.models import Post, Category
from django.urls import reverse
from django.urls import reverse_lazy
from django.urls import reverse
from django.urls import reverse_lazy

def home(request):
    """
    Home page view that shows recent activity and community highlights.
    """
    # Get recent posts from the community
    recent_posts = Post.objects.select_related('author', 'category').order_by('-created_at')[:5]
    
    # Get active categories
    categories = Category.objects.all()[:6]
    
    context = {
        'recent_posts': recent_posts,
        'categories': categories,
        'page_title': 'Welcome to Our Community',
    }
    return render(request, 'core/home.html', context)

@login_required
def dashboard(request):
    """Display user's dashboard with their posts and messages."""
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    messages = UserMessage.objects.filter(recipient=request.user).order_by('-created_at')
    
    context = {
        'forum_posts': posts,
        'user_messages': messages,
    }
    return render(request, 'dashboard.html', context) 