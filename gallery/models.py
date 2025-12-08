from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Tag(models.Model):
    """Tag for categorizing artwork"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        """Auto-generate slug from name"""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Artwork(models.Model):
    """User-uploaded artwork"""
    artist = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='artworks'
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.URLField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='artworks')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} by {self.artist.username}"
