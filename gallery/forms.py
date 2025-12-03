from django import forms
from .models import Artwork


class ArtworkForm(forms.ModelForm):
    """Form for uploading artwork with tag input"""
    # Text input for tags: "anime, sketch, oc"
    tags_input = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. anime, sketch, oc', 
            'class': 'form-input'
        }),
        label='Tags (comma separated)'
    )

    class Meta:
        model = Artwork
        fields = ['title', 'description', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Give your artwork a title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input', 
                'rows': 4,
                'placeholder': 'Describe your artwork...'
            }),
            'image': forms.FileInput(attrs={'class': 'form-file'}),
        }
