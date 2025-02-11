from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from .models import Post, Vote, Comment
from .forms import PostForm, CommentForm

@login_required
def post_list(request):
    """
    List posts for the forum.
    - Staff users see both posts and submissions.
    - Other users see only posts (type 'post').
    """
    if request.user.is_staff:
        posts = Post.objects.all().order_by('-created_at')
    else:
        posts = Post.objects.filter(type='post').order_by('-created_at')
    return render(request, 'forum/post_list.html', {'posts': posts})


@login_required
def create_post(request):
    """
    Allow a user to create a post.
    If a non-staff user tries to create a submission, force it to be a post.
    """
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # Enforce that only staff posts can be submissions
            if not request.user.is_staff and post.type == 'submission':
                post.type = 'post'
            post.save()
            return redirect('forum:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'forum/create_post.html', {'form': form})


@login_required
def post_detail(request, pk):
    """
    Show a single post with its comments and a form to add a comment.
    For submissions, only staff should be allowed to view.
    """
    post = get_object_or_404(Post, pk=pk)
    if post.type == 'submission' and not request.user.is_staff:
        raise Http404("Submission not available")
    comments = post.comments.all().order_by('created_at')
    comment_form = CommentForm()
    return render(
        request,
        'forum/post_detail.html',
        {'post': post, 'comments': comments, 'comment_form': comment_form}
    )


@login_required
def add_comment(request, pk):
    """
    Add a comment to a post.
    """
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
    return redirect('forum:post_detail', pk=post.pk)


@login_required
def vote_post(request, pk, vote_type):
    """
    Upvote or downvote a post.
    vote_type should be either 'up' or 'down'. If a user votes the same
    way twice, we remove the vote (toggle off).
    """
    post = get_object_or_404(Post, pk=pk)
    # Determine vote value from the vote_type parameter
    if vote_type == 'up':
        value = 1
    elif vote_type == 'down':
        value = -1
    else:
        # Use the forum namespace for the redirect
        return redirect('forum:post_detail', pk=pk)

    vote, created = Vote.objects.get_or_create(
        post=post, user=request.user, defaults={'value': value}
    )
    if not created:
        if vote.value == value:
            # Remove vote if already cast in the same direction
            vote.delete()
        else:
            # Update vote to the new value
            vote.value = value
            vote.save()

    # Redirect using the namespaced URL
    return redirect('forum:post_detail', pk=pk)
