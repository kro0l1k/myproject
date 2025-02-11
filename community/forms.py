from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    """Form for creating and editing posts."""
    
    class Meta:
        model = Post
        fields = ['category', 'title', 'content', 'type']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'content-editor'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        self.fields['type'].widget.attrs.update({'class': 'form-select'})
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        
        # Only staff members can create announcements
        user = kwargs.get('initial', {}).get('user')
        if user and not user.is_staff:
            type_choices = [choice for choice in self.fields['type'].choices if choice[0] != 'announcement']
            self.fields['type'].choices = type_choices

class CommentForm(forms.ModelForm):
    """Form for creating and editing comments."""
    
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'class': 'form-control',
                'placeholder': 'Write your comment here...'
            }),
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content.strip()) < 2:
            raise forms.ValidationError("Comment must contain at least 2 characters.")
        return content 