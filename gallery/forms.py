from django import forms
from .models import Artwork, Category


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

    # Manually add the image field so it's not tied to the model's URLField
    image = forms.ImageField(
        required=True, 
        widget=forms.FileInput(attrs={'class': 'form-file'})
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-input'}),
        empty_label="Select a category..."
    )

    class Meta:
        model = Artwork
        # 'image' is removed from here because we handle it manually
        fields = ['title', 'description', 'category']
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
        }


class ArtworkEditForm(forms.ModelForm):
    """Form for editing artwork (no image change allowed)"""
    tags_input = forms.CharField(
        required=False, 
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g. anime, sketch, oc', 
            'class': 'form-input'
        }),
        label='Tags (comma separated)'
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-input'}),
        empty_label="Select a category..."
    )

    class Meta:
        model = Artwork
        fields = ['title', 'description', 'category']
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
        }
