from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    """Admin-managed category for structured artwork organization"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    icon = models.CharField(max_length=10, default='🎨', help_text="Emoji icon for the category")
    order = models.PositiveIntegerField(default=0, help_text="Display order (lower = first)")
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.icon} {self.name}"


class Tag(models.Model):
    """Tag for freeform artwork categorization by users"""
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
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='artworks'
    )
    # URL-based image (for Supabase storage)
    image = models.URLField(max_length=1000, blank=True)
    # Local file-based image (for local development)
    image_file = models.ImageField(upload_to='artworks/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name='artworks')

    class Meta:
        ordering = ['-created_at']

    @property
    def get_image_url(self):
        """Return the appropriate image URL based on storage method"""
        if self.image_file:
            return self.image_file.url
        return self.image

    def __str__(self):
        return f"{self.title} by {self.artist.username}"
