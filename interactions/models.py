from django.db import models
from django.conf import settings
from gallery.models import Artwork


class Like(models.Model):
    """Like on an artwork"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    artwork = models.ForeignKey(
        Artwork, 
        on_delete=models.CASCADE, 
        related_name='likes'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'artwork')

    def __str__(self):
        return f"{self.user.username} likes {self.artwork.title}"


class Comment(models.Model):
    """Comment on an artwork"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    content = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Track if artwork owner has seen this
    is_pinned = models.BooleanField(default=False) # Track if the artwork owner pinned this

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} on {self.artwork.title}"


class Report(models.Model):
    """Report on an artwork for content moderation"""
    REASON_CHOICES = [
        ('inappropriate', 'Inappropriate Content'),
        ('spam', 'Spam'),
        ('harassment', 'Harassment'),
        ('copyright', 'Copyright Violation'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Under Review'),
        ('dismissed', 'Dismissed'),
        ('resolved', 'Resolved - Action Taken'),
    ]
    
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports_made'
    )
    artwork = models.ForeignKey(
        Artwork,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports'
    )
    artwork_title_backup = models.CharField(max_length=200, blank=True, help_text="Backup of artwork title if deleted")
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    description = models.TextField(max_length=500, blank=True, help_text="Optional additional details")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True, help_text="Internal notes for admins")
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_resolved'
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Report on {self.artwork.title} by {self.reporter.username}"


class CommentFlag(models.Model):
    """Tracks community flags on comments"""
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='flags'
    )
    flagged_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comment_flags_given'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'flagged_by')
        
    def __str__(self):
        return f"Flag by {self.flagged_by.username} on comment {self.comment.id}"
