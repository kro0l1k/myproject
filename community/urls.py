from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    # Category views
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Post views
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/create/', views.PostCreateView.as_view(), name='post_create'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Comment views
    path('posts/<int:post_pk>/comment/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comments/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),
    path('comments/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('comments/<int:pk>/reply/', views.CommentReplyView.as_view(), name='comment_reply'),
    
    # Voting
    path('posts/<int:pk>/vote/', views.PostVoteView.as_view(), name='post_vote'),
    
    # API endpoints for AJAX functionality
    path('api/posts/<int:pk>/vote/', views.post_vote_api, name='api_post_vote'),
    path('api/posts/<int:pk>/view/', views.post_view_api, name='api_post_view'),
] 