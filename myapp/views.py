from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from .models import ForumPost, UserMessage

@staff_member_required
def admin_dashboard(request):
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
    }
    return render(request, 'dashboard.html', context) 