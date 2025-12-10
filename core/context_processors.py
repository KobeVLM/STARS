"""
Context processor to clear gamification session variables after they've been displayed.
"""


def clear_xp_session(request):
    """Clear XP-related session variables after template render"""
    xp_gained = request.session.pop('xp_gained', None)
    xp_action = request.session.pop('xp_action', None)
    level_up = request.session.pop('level_up', None)
    new_badges = request.session.pop('new_badges', None)
    
    # If no session badges, check database for unshown badge notifications
    if not new_badges and request.user.is_authenticated:
        from users.models import UserBadge
        unshown_badges = UserBadge.objects.filter(
            user=request.user, 
            notification_shown=False
        ).select_related('badge')
        
        if unshown_badges.exists():
            new_badges = [
                {
                    'name': ub.badge.name, 
                    'icon': ub.badge.icon, 
                    'xp': ub.badge.xp_reward, 
                    'description': ub.badge.description
                }
                for ub in unshown_badges
            ]
            # Mark as shown
            unshown_badges.update(notification_shown=True)
    
    return {
        'xp_gained': xp_gained,
        'xp_action': xp_action,
        'level_up': level_up,
        'new_badges': new_badges,
    }
