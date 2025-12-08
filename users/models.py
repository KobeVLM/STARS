import math
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """Extended user model with gamification features"""
    bio = models.TextField(blank=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # Gamification
    xp = models.IntegerField(default=0)
    level = models.IntegerField(default=1)

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
        """Award XP and automatically level up if threshold reached"""
        self.xp += points
        new_level = self.calculate_level()
        if new_level > self.level:
            self.level = new_level
            self.save()
            return True
        self.save()
        return False

    def __str__(self):
        return self.username


class Badge(models.Model):
    """Achievement badge that users can unlock"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🏆')  # Emoji icon
    
    # Unlock criteria
    criteria_type = models.CharField(max_length=50, choices=[
        ('uploads', 'Number of uploads'),
        ('likes_given', 'Number of likes given'),
        ('likes_received', 'Number of likes received'),
        ('level', 'User level'),
        ('comments', 'Number of comments'),
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
    
    class Meta:
        unique_together = ('user', 'badge')
        ordering = ['-earned_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.badge.name}"
