"""
Context processor to clear gamification session variables after they've been displayed.
"""


def clear_xp_session(request):
    """Clear XP-related session variables after template render"""
    xp_gained = request.session.pop('xp_gained', None)
    xp_action = request.session.pop('xp_action', None)
    level_up = request.session.pop('level_up', None)
    new_badges = request.session.pop('new_badges', None)
    
    return {
        'xp_gained': xp_gained,
        'xp_action': xp_action,
        'level_up': level_up,
        'new_badges': new_badges,
    }

