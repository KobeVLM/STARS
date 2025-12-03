from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileEditForm
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
        form = CustomUserCreationForm()
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
