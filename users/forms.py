from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """Form for user registration"""
    email = forms.EmailField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')


class ProfileEditForm(forms.ModelForm):
    """Form for editing user profile"""
    class Meta:
        model = CustomUser
        fields = ('bio', 'avatar')
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'form-input',
                'rows': 4,
                'placeholder': 'Tell us about yourself...'
            }),
            'avatar': forms.FileInput(attrs={'class': 'form-input'}),
        }


class AccountSettingsForm(forms.Form):
    """Form for updating account settings"""
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Email address'
        })
    )
    username = forms.CharField(
        required=False,
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username'
        })
    )
    current_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Current password'
        })
    )
    new_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'New password'
        })
    )
    confirm_password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm new password'
        })
    )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        # Set initial values
        self.fields['email'].initial = user.email
        self.fields['username'].initial = user.username

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username and username != self.user.username:
            if CustomUser.objects.filter(username=username).exists():
                raise forms.ValidationError('This username is already taken.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        current_password = cleaned_data.get('current_password')
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        # If trying to change password
        if new_password or confirm_password:
            if not current_password:
                raise forms.ValidationError('Please enter your current password to change your password.')
            
            if not self.user.check_password(current_password):
                raise forms.ValidationError('Current password is incorrect.')
            
            if new_password != confirm_password:
                raise forms.ValidationError('New passwords do not match.')
            
            if len(new_password) < 8:
                raise forms.ValidationError('New password must be at least 8 characters long.')

        return cleaned_data
