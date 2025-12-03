from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileEditForm, AccountSettingsForm
from .models import CustomUser


def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome')
    else:
        form = CustomUserCreationForm(request.POST)
    return render(request, 'users/register.html', {'form': form})


def welcome(request):
    """Welcome/onboarding page after registration"""
    return render(request, 'core/welcome.html')


@login_required
def profile_view(request, username):
    """Display user profile"""
    user = get_object_or_404(CustomUser, username=username)
    artworks = user.artworks.all()
    
    # Calculate XP progress to next level
    xp_for_current_level = (user.level - 1) * 100
    xp_for_next_level = user.level * 100
    xp_progress = user.xp - xp_for_current_level
    xp_needed = xp_for_next_level - xp_for_current_level
    xp_percentage = (xp_progress / xp_needed) * 100 if xp_needed > 0 else 0
    
    context = {
        'profile_user': user,
        'artworks': artworks,
        'xp_percentage': xp_percentage,
        'xp_progress': xp_progress,
        'xp_needed': xp_needed,
        'xp_for_next_level': xp_for_next_level,
    }
    return render(request, 'users/profile.html', context)


@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # Award XP for completing profile
            if request.user.bio and request.user.avatar:
                request.user.award_xp(20)
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileEditForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})


@login_required
def account_settings(request):
    """Account settings - update email, username, password"""
    if request.method == 'POST':
        form = AccountSettingsForm(request.user, request.POST)
        if form.is_valid():
            user = request.user
            updated = False
            
            # Update email
            new_email = form.cleaned_data.get('email')
            if new_email and new_email != user.email:
                user.email = new_email
                updated = True
                messages.success(request, 'Email updated successfully!')
            
            # Update username
            new_username = form.cleaned_data.get('username')
            if new_username and new_username != user.username:
                user.username = new_username
                updated = True
                messages.success(request, 'Username updated successfully!')
            
            # Update password
            new_password = form.cleaned_data.get('new_password')
            if new_password:
                user.set_password(new_password)
                updated = True
                messages.success(request, 'Password updated successfully! Please log in again.')
                user.save()
                # Log out user after password change
                logout(request)
                return redirect('login')
            
            if updated:
                user.save()
                return redirect('account_settings')
            else:
                messages.info(request, 'No changes were made.')
    else:
        form = AccountSettingsForm(request.user)
    
    return render(request, 'users/account_settings.html', {'form': form})
