from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender='gallery.Artwork')
def award_upload_xp(sender, instance, created, **kwargs):
    """Award XP when user uploads artwork"""
    if created:
        instance.artist.award_xp(50)  # +50 XP for Upload
        
        # Check for badge unlocks
        from .badge_utils import check_and_award_badges
        check_and_award_badges(instance.artist)


@receiver(post_save, sender='interactions.Like')
def award_like_xp(sender, instance, created, **kwargs):
    """Award XP when user likes artwork and to artwork owner"""
    if created:
        # Award XP to user who liked
        instance.user.award_xp(10)  # +10 XP for Liking
        
        # Award XP to artwork owner for receiving a like
        instance.artwork.artist.award_xp(5)  # +5 XP for receiving a like
        
        # Check for badge unlocks for both users
        from .badge_utils import check_and_award_badges
        check_and_award_badges(instance.user)
        check_and_award_badges(instance.artwork.artist)


@receiver(post_save, sender='interactions.Comment')
def award_comment_xp(sender, instance, created, **kwargs):
    """Award XP when user comments"""
    if created:
        # XP already awarded in view, just check badges
        from .badge_utils import check_and_award_badges
        check_and_award_badges(instance.user)
