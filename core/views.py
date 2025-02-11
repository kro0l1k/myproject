from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import ForumPost, UserMessage
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
def admin_dashboard(request):
    """
    Admin dashboard view for site management.
    """
    if not request.user.is_staff:
        return reverse('core:home')
        
    try:
        forum_posts = ForumPost.objects.all().order_by('-created_at')
    except:
        forum_posts = []
        
    try:
        user_messages = UserMessage.objects.all().order_by('-sent_at')
    except:
        user_messages = []
    
    context = {
        'forum_posts': forum_posts,
        'user_messages': user_messages,
        'page_title': 'Admin Dashboard',
    }
    return render(request, 'dashboard.html', context) 