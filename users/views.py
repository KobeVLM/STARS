from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .forms import CustomUserCreationForm, ProfileEditForm, AccountSettingsForm
from .models import CustomUser, Follow, Badge, UserBadge
from gallery.models import Artwork
from interactions.models import Like, Comment


def check_and_award_badges(user, request=None):
    """Check if user qualifies for any badges and award them + XP"""
    newly_earned = []
    
    # Get all badges user hasn't earned yet
    earned_badge_ids = UserBadge.objects.filter(user=user).values_list('badge_id', flat=True)
    available_badges = Badge.objects.exclude(id__in=earned_badge_ids)
    
    for badge in available_badges:
        qualified = False
        
        if badge.criteria_type == 'uploads':
            count = user.artworks.count()
            qualified = count >= badge.criteria_value
        elif badge.criteria_type == 'likes_given':
            count = Like.objects.filter(user=user).count()
            qualified = count >= badge.criteria_value
        elif badge.criteria_type == 'likes_received':
            count = Like.objects.filter(artwork__artist=user).count()
            qualified = count >= badge.criteria_value
        elif badge.criteria_type == 'level':
            qualified = user.level >= badge.criteria_value
        elif badge.criteria_type == 'comments':
            count = Comment.objects.filter(user=user).count()
            qualified = count >= badge.criteria_value
        elif badge.criteria_type == 'followers':
            count = user.followers.count()
            qualified = count >= badge.criteria_value
        
        if qualified:
            # Award the badge
            UserBadge.objects.create(user=user, badge=badge, notification_shown=False)
            newly_earned.append(badge)
            
            # Award XP from badge
            if badge.xp_reward > 0:
                user.award_xp(badge.xp_reward)
    
    # Store newly earned badges in session for popup
    if request and newly_earned:
        request.session['new_badges'] = [
            {'name': b.name, 'icon': b.icon, 'xp': b.xp_reward, 'description': b.description}
            for b in newly_earned
        ]
    
    return newly_earned


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
def dashboard(request):
    """User dashboard - the main hub after login"""
    user = request.user
    
    # Update daily streak
    streak_updated, is_new_streak, bonus_xp = user.update_streak()
    if bonus_xp > 0:
        leveled_up, new_level = user.award_xp(bonus_xp)
        request.session['xp_gained'] = bonus_xp
        request.session['xp_action'] = f'day {user.streak_count} streak bonus'
        if leveled_up:
            request.session['level_up'] = new_level
    
    # Check for new badges
    check_and_award_badges(user, request)
    
    # User's stats
    user_artworks = user.artworks.all()
    total_artworks = user_artworks.count()
    total_likes_received = Like.objects.filter(artwork__artist=user).count()
    
    # Unread comments count
    unread_comments = Comment.objects.filter(
        artwork__artist=user,
        is_read=False
    ).exclude(user=user).count()
    
    # Calculate XP progress to next level
    xp_for_current_level = (user.level - 1) ** 2 * 100
    xp_for_next_level = user.level ** 2 * 100
    xp_progress = user.xp - xp_for_current_level
    xp_needed = xp_for_next_level - xp_for_current_level
    xp_percentage = (xp_progress / xp_needed) * 100 if xp_needed > 0 else 0
    
    # Trending artworks (most liked, from other users, recent)
    trending_artworks = Artwork.objects.exclude(artist=user).annotate(
        like_count=Count('likes')
    ).order_by('-like_count', '-created_at')[:6]
    
    # Artworks from users I follow (new from followed artists)
    followed_user_ids = user.following.values_list('followed_id', flat=True)
    followed_artworks = Artwork.objects.filter(
        artist_id__in=followed_user_ids
    ).order_by('-created_at')[:6]
    
    # User's recent artworks
    recent_artworks = user_artworks[:3]
    
    context = {
        'user': user,
        'total_artworks': total_artworks,
        'total_likes_received': total_likes_received,
        'unread_comments': unread_comments,
        'xp_percentage': xp_percentage,
        'xp_progress': xp_progress,
        'xp_needed': xp_needed,
        'trending_artworks': trending_artworks,
        'followed_artworks': followed_artworks,
        'recent_artworks': recent_artworks,
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def profile_view(request, username):
    """Display user profile"""
    profile_user = get_object_or_404(CustomUser, username=username)
    artworks = profile_user.artworks.all()
    
    # Calculate XP progress to next level
    # Formula: Required XP = (level - 1)² × 100
    xp_for_current_level = (profile_user.level - 1) ** 2 * 100
    xp_for_next_level = profile_user.level ** 2 * 100
    xp_progress = profile_user.xp - xp_for_current_level
    xp_needed = xp_for_next_level - xp_for_current_level
    xp_percentage = (xp_progress / xp_needed) * 100 if xp_needed > 0 else 0
    
    # Follower/Following stats
    followers_count = profile_user.followers.count()
    following_count = profile_user.following.count()
    
    # Check if current user is following this profile
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = Follow.objects.filter(
            follower=request.user, 
            followed=profile_user
        ).exists()
    
    context = {
        'profile_user': profile_user,
        'artworks': artworks,
        'xp_percentage': xp_percentage,
        'xp_progress': xp_progress,
        'xp_needed': xp_needed,
        'xp_for_next_level': xp_for_next_level,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
    }
    return render(request, 'users/profile.html', context)


@login_required
def toggle_follow(request, username):
    """Follow or unfollow a user"""
    target_user = get_object_or_404(CustomUser, username=username)
    
    # Can't follow yourself
    if target_user == request.user:
        messages.error(request, "You can't follow yourself!")
        return redirect('profile', username=username)
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        followed=target_user
    )
    
    if not created:
        # Already following, so unfollow
        follow.delete()
        messages.success(request, f'You unfollowed {target_user.username}')
    else:
        # Now following
        messages.success(request, f'You are now following {target_user.username}!')
        # Check if target user qualifies for follower badges
        check_and_award_badges(target_user)
    
    return redirect('profile', username=username)


@login_required
def profile_edit(request):
    """Edit user profile"""
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            # Award XP for completing profile (first time only)
            if request.user.bio and request.user.avatar:
                leveled_up, new_level = request.user.award_xp(20)
                request.session['xp_gained'] = 20
                request.session['xp_action'] = 'completing profile'
                if leveled_up:
                    request.session['level_up'] = new_level
            messages.success(request, "Your profile has been updated successfully!")
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


@login_required
def followers_list(request, username):
    """Show list of users who follow this profile"""
    profile_user = get_object_or_404(CustomUser, username=username)
    followers = Follow.objects.filter(followed=profile_user).select_related('follower')
    
    # Get IDs of users the current user follows
    my_following_ids = list(request.user.following.values_list('followed_id', flat=True))
    
    context = {
        'profile_user': profile_user,
        'users_list': [f.follower for f in followers],
        'my_following_ids': my_following_ids,
        'list_type': 'Followers',
    }
    return render(request, 'users/follow_list.html', context)


@login_required
def following_list(request, username):
    """Show list of users this profile follows"""
    profile_user = get_object_or_404(CustomUser, username=username)
    following = Follow.objects.filter(follower=profile_user).select_related('followed')
    
    # Get IDs of users the current user follows
    my_following_ids = list(request.user.following.values_list('followed_id', flat=True))
    
    context = {
        'profile_user': profile_user,
        'users_list': [f.followed for f in following],
        'my_following_ids': my_following_ids,
        'list_type': 'Following',
    }
    return render(request, 'users/follow_list.html', context)

