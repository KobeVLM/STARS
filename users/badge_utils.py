"""Utility functions for badge checking and awarding"""
from .models import Badge, UserBadge


def check_and_award_badges(user):
    """Check if user qualifies for any new badges and award them"""
    from gallery.models import Artwork
    from interactions.models import Like, Comment
    
    # Get user stats
    stats = {
        'uploads': Artwork.objects.filter(artist=user).count(),
        'likes_given': Like.objects.filter(user=user).count(),
        'likes_received': Like.objects.filter(artwork__artist=user).count(),
        'level': user.level,
        'comments': Comment.objects.filter(user=user).count(),
    }
    
    # Get all badges
    all_badges = Badge.objects.all()
    
    # Get badges user already has
    earned_badge_ids = user.earned_badges.values_list('badge_id', flat=True)
    
    newly_awarded = []
    
    for badge in all_badges:
        # Skip if user already has this badge
        if badge.id in earned_badge_ids:
            continue
        
        # Check if user meets criteria
        user_stat = stats.get(badge.criteria_type, 0)
        if user_stat >= badge.criteria_value:
            # Award badge
            UserBadge.objects.create(user=user, badge=badge)
            newly_awarded.append(badge)
    
    return newly_awarded
