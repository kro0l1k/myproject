from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse
from django.db.models import F
from django.contrib import messages
from .models import Category, Post, Comment, Vote
from .forms import PostForm, CommentForm

class CategoryListView(ListView):
    """Display all categories in the community forum."""
    model = Category
    context_object_name = 'categories'
    template_name = 'community/category_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for category in context['categories']:
            category.post_count = category.posts.count()
            category.latest_post = category.posts.order_by('-created_at').first()
        return context

class CategoryDetailView(DetailView):
    """Display posts within a specific category."""
    model = Category
    context_object_name = 'category'
    template_name = 'community/category_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = self.object.posts.order_by('-is_pinned', '-last_activity')
        return context

class PostListView(ListView):
    """Display all posts across all categories."""
    model = Post
    context_object_name = 'posts'
    template_name = 'community/post_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.select_related('author', 'category').order_by('-is_pinned', '-last_activity')

class PostDetailView(FormMixin, DetailView):
    """Display a single post and its comments."""
    model = Post
    context_object_name = 'post'
    template_name = 'community/post_detail.html'
    form_class = CommentForm
    
    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        if not request.session.get(f'post_viewed_{self.object.pk}'):
            Post.objects.filter(pk=self.object.pk).update(views_count=F('views_count') + 1)
            request.session[f'post_viewed_{self.object.pk}'] = True
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.select_related('author').filter(parent=None)
        if self.request.user.is_authenticated:
            context['user_vote'] = self.object.votes.filter(user=self.request.user).first()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new post."""
    model = Post
    form_class = PostForm
    template_name = 'community/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        
        # Handle new category creation
        if self.request.POST.get('category') == 'new':
            category_name = self.request.POST.get('new_category_name')
            category_description = self.request.POST.get('new_category_description')
            
            if category_name:
                from django.utils.text import slugify
                category = Category.objects.create(
                    name=category_name,
                    description=category_description or '',
                    slug=slugify(category_name)
                )
                form.instance.category = category
            else:
                form.add_error('category', 'Please provide a name for the new category')
                return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('community:post_detail', kwargs={'pk': self.object.pk})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing post."""
    model = Post
    form_class = PostForm
    template_name = 'community/post_form.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a post."""
    model = Post
    success_url = reverse_lazy('community:post_list')
    template_name = 'community/post_confirm_delete.html'
    
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author or self.request.user.is_staff

class CommentCreateView(LoginRequiredMixin, CreateView):
    """Create a new comment on a post."""
    model = Comment
    form_class = CommentForm
    template_name = 'community/comment_form.html'
    
    def form_valid(self, form):
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        form.instance.post = post
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('community:post_detail', kwargs={'pk': self.kwargs['post_pk']})

class CommentReplyView(LoginRequiredMixin, CreateView):
    """Reply to an existing comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'community/comment_form.html'
    
    def form_valid(self, form):
        parent_comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        form.instance.post = parent_comment.post
        form.instance.parent = parent_comment
        form.instance.author = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('community:post_detail', kwargs={'pk': self.object.post.pk})

class PostVoteView(LoginRequiredMixin, UpdateView):
    """Handle post voting."""
    model = Post
    fields = []  # No fields needed as we're just handling the vote
    
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        value = int(request.POST.get('value'))
        
        vote, created = Vote.objects.get_or_create(
            post=post,
            user=request.user,
            defaults={'value': value}
        )
        
        if not created:
            if vote.value == value:
                vote.delete()
            else:
                vote.value = value
                vote.save()
        
        return JsonResponse({
            'score': post.vote_score(),
            'status': 'success'
        })

@login_required
def post_vote_api(request, pk):
    """API endpoint for voting on posts."""
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=pk)
        value = int(request.POST.get('value'))
        
        vote, created = Vote.objects.get_or_create(
            post=post,
            user=request.user,
            defaults={'value': value}
        )
        
        if not created:
            if vote.value == value:
                vote.delete()
            else:
                vote.value = value
                vote.save()
        
        return JsonResponse({
            'score': post.vote_score(),
            'status': 'success'
        })
    return JsonResponse({'status': 'error'}, status=400)

@login_required
def post_view_api(request, pk):
    """API endpoint for tracking post views."""
    if request.method == 'POST':
        if not request.session.get(f'post_viewed_{pk}'):
            Post.objects.filter(pk=pk).update(views_count=F('views_count') + 1)
            request.session[f'post_viewed_{pk}'] = True
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update an existing comment."""
    model = Comment
    form_class = CommentForm
    template_name = 'community/comment_form.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_staff
    
    def get_success_url(self):
        return reverse('community:post_detail', kwargs={'pk': self.object.post.pk})

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Delete a comment."""
    model = Comment
    template_name = 'community/comment_confirm_delete.html'
    
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author or self.request.user.is_staff
    
    def get_success_url(self):
        return reverse('community:post_detail', kwargs={'pk': self.object.post.pk})
