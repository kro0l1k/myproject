document.addEventListener('DOMContentLoaded', function() {
    // Handle voting
    const voteButtons = document.querySelectorAll('.vote-button');
    voteButtons.forEach(button => {
        button.addEventListener('click', handleVote);
    });

    // Handle post view counting
    const postContent = document.querySelector('.post-content');
    if (postContent) {
        trackPostView();
    }
});

function handleVote(event) {
    event.preventDefault();
    const button = event.currentTarget;
    const postId = button.dataset.postId;
    const voteValue = parseInt(button.dataset.voteValue);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/community/api/posts/${postId}/vote/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        },
        body: `value=${voteValue}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Update vote score
            const scoreElement = button.closest('.vote-buttons').querySelector('.vote-score');
            scoreElement.textContent = data.score;

            // Toggle active state
            const voteButtons = button.closest('.vote-buttons').querySelectorAll('.vote-button');
            voteButtons.forEach(btn => btn.classList.remove('active'));
            
            if (data.score !== 0) {
                button.classList.add('active');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function trackPostView() {
    const postId = document.querySelector('[data-post-id]').dataset.postId;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/community/api/posts/${postId}/view/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': csrfToken
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Comment functionality
function showReplyForm(commentId) {
    const replyForm = document.getElementById(`reply-form-${commentId}`);
    if (replyForm) {
        replyForm.style.display = replyForm.style.display === 'none' ? 'block' : 'none';
    }
}

function enableCommentEdit(commentId) {
    const contentDiv = document.getElementById(`comment-content-${commentId}`);
    const editForm = document.getElementById(`edit-form-${commentId}`);
    if (contentDiv && editForm) {
        contentDiv.style.display = 'none';
        editForm.style.display = 'block';
    }
}

function cancelCommentEdit(commentId) {
    const contentDiv = document.getElementById(`comment-content-${commentId}`);
    const editForm = document.getElementById(`edit-form-${commentId}`);
    if (contentDiv && editForm) {
        contentDiv.style.display = 'block';
        editForm.style.display = 'none';
    }
}

// Dynamic comment loading
function loadMoreComments(postId, page) {
    const commentsContainer = document.querySelector('.comments-container');
    const loadMoreBtn = document.querySelector('.load-more-comments');
    
    fetch(`/community/posts/${postId}/comments/?page=${page}`)
        .then(response => response.json())
        .then(data => {
            commentsContainer.insertAdjacentHTML('beforeend', data.html);
            if (!data.has_next) {
                loadMoreBtn.style.display = 'none';
            } else {
                loadMoreBtn.dataset.page = page + 1;
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
}

// Post preview
const markdownPreview = document.querySelector('.markdown-preview');
if (markdownPreview) {
    const contentEditor = document.querySelector('.content-editor');
    contentEditor.addEventListener('input', debounce(function() {
        fetch('/community/api/preview/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: `content=${encodeURIComponent(this.value)}`
        })
        .then(response => response.json())
        .then(data => {
            markdownPreview.innerHTML = data.html;
        });
    }, 300));
}

// Utility function for debouncing
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func.apply(this, args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Helper function to get CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
} 