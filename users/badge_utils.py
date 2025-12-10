"""Utility functions for badge checking and awarding"""
from .models import Badge, UserBadge


def check_and_award_badges(user, request=None):
    """Check if user qualifies for any new badges and award them with XP"""
    from gallery.models import Artwork
    from interactions.models import Like, Comment
    from users.models import Follow
    
    # Get user stats
    stats = {
        'uploads': Artwork.objects.filter(artist=user).count(),
        'likes_given': Like.objects.filter(user=user).count(),
        'likes_received': Like.objects.filter(artwork__artist=user).count(),
        'level': user.level,
        'comments': Comment.objects.filter(user=user).count(),
        'followers': Follow.objects.filter(followed=user).count(),
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
            UserBadge.objects.create(user=user, badge=badge, notification_shown=False)
            newly_awarded.append(badge)
            
            # Award XP from badge
            if badge.xp_reward > 0:
                user.award_xp(badge.xp_reward)
    
    # Store newly earned badges in session for popup notification
    if request and newly_awarded:
        request.session['new_badges'] = [
            {'name': b.name, 'icon': b.icon, 'xp': b.xp_reward, 'description': b.description}
            for b in newly_awarded
        ]
    
    return newly_awarded

