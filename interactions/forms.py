from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    """Form for posting comments on artwork"""
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 3,
                'placeholder': 'Share your thoughts...',
            }),
        }
        labels = {
            'content': 'Add a comment'
        }
