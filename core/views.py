from django.shortcuts import render
from users.models import CustomUser


def landing(request):
    """Landing page"""
    return render(request, 'core/landing.html')


def welcome(request):
    """Welcome/onboarding page"""
    return render(request, 'core/welcome.html')


def leaderboard(request):
    """Leaderboard - Top artists by XP"""
    # Get top 20 users by XP
    top_users = CustomUser.objects.order_by('-xp')[:20]
    
    # Get current user's rank if authenticated
    user_rank = None
    if request.user.is_authenticated:
        # Count users with higher XP
        higher_xp_count = CustomUser.objects.filter(xp__gt=request.user.xp).count()
        user_rank = higher_xp_count + 1
    
    context = {
        'top_users': top_users,
        'user_rank': user_rank,
    }
    return render(request, 'core/leaderboard.html', context)

