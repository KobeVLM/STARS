import math
from datetime import date, timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model with gamification features"""
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Gamification
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    
    # Daily Streak
    last_login_date = models.DateField(null=True, blank=True)
    streak_count = models.IntegerField(default=0)

    def calculate_level(self):
        """Calculate level based on XP using square root formula
        
        Formula: Level = sqrt(total_xp / 100) + 1
        This provides a more balanced progression curve where higher levels
        require exponentially more XP to achieve.
        """
        # Level = sqrt(total_xp / 100) + 1
        new_level = max(1, int(math.sqrt(self.xp / 100)) + 1)
        return new_level

    def award_xp(self, points):
        """Award XP and automatically level up if threshold reached
        
        Returns:
            tuple: (leveled_up: bool, new_level: int)
        """
        self.xp += points
        new_level = self.calculate_level()
        leveled_up = False
        if new_level > self.level:
            self.level = new_level
            leveled_up = True
        self.save()
        return (leveled_up, new_level)

    def update_streak(self):
        """Update daily login streak. Returns (streak_updated, is_new_streak, bonus_xp)"""
        today = date.today()
        bonus_xp = 0
        is_new_streak = False
        streak_updated = False
        
        if self.last_login_date is None:
            # First ever login
            self.streak_count = 1
            self.last_login_date = today
            is_new_streak = True
            streak_updated = True
        elif self.last_login_date == today:
            # Already logged in today, no change
            pass
        elif self.last_login_date == today - timedelta(days=1):
            # Consecutive day - increase streak!
            self.streak_count += 1
            self.last_login_date = today
            is_new_streak = True
            streak_updated = True
            # Bonus XP: +10 XP per streak day (max 50 XP at 5 day streak)
            bonus_xp = min(self.streak_count * 10, 50)
        else:
            # Streak broken - reset to 1
            self.streak_count = 1
            self.last_login_date = today
            streak_updated = True
        
        if streak_updated:
            self.save()
        
        return (streak_updated, is_new_streak, bonus_xp)

    def __str__(self):
        return self.username


class Follow(models.Model):
    """Follow relationship between users"""
    follower = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='following'  # Users I follow
    )
    followed = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='followers'  # Users who follow me
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"


class Badge(models.Model):
    """Achievement badge that users can unlock"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🏆')  # Emoji icon
    
    # XP reward when badge is unlocked
    xp_reward = models.IntegerField(default=50)
    
    # Unlock criteria
    criteria_type = models.CharField(max_length=50, choices=[
        ('uploads', 'Number of uploads'),
        ('likes_given', 'Number of likes given'),
        ('likes_received', 'Number of likes received'),
        ('level', 'User level'),
        ('comments', 'Number of comments'),
        ('followers', 'Number of followers'),
    ])
    criteria_value = models.IntegerField()  # Threshold to unlock
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['criteria_value']
    
    def __str__(self):
        return f"{self.icon} {self.name}"


class UserBadge(models.Model):
    """Tracks which badges a user has earned"""
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='earned_badges'
    )
    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name='users'
    )
    earned_at = models.DateTimeField(auto_now_add=True)
    notification_shown = models.BooleanField(default=False)  # Track if popup was shown
    
    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"

