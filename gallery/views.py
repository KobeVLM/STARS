from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages
from django.conf import settings as django_settings
from .models import Artwork, Tag, Category
from .forms import ArtworkForm, ArtworkEditForm
from interactions.forms import CommentForm
import os
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Supabase client setup (only when not using local storage)
supabase = None
if not getattr(django_settings, 'USE_LOCAL_STORAGE', False):
    try:
        from supabase import create_client, Client
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        if url and key:
            supabase: Client = create_client(url, key)
    except ImportError:
        logger.warning("Supabase library not installed, using local storage only")


def explore_feed(request):
    """Main gallery feed with search and category-based carousel sections"""
    
    # Search by title, artist username, or tags
    query = request.GET.get('q')
    
    # Get all categories with their artworks
    categories_with_artworks = []
    for category in Category.objects.all().order_by('order', 'name'):
        artworks = Artwork.objects.filter(category=category).select_related('artist').prefetch_related('tags', 'likes').order_by('-created_at')
        
        # Apply search filter if present
        if query:
            artworks = artworks.filter(
                Q(title__icontains=query) | 
                Q(artist__username__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        
        categories_with_artworks.append({
            'category': category,
            'artworks': list(artworks),  # Convert to list for template
            'count': artworks.count()
        })
    
    # Get IDs of artworks the current user has liked
    user_liked_ids = []
    if request.user.is_authenticated:
        from interactions.models import Like
        user_liked_ids = list(Like.objects.filter(user=request.user).values_list('artwork_id', flat=True))

    context = {
        'categories_with_artworks': categories_with_artworks,
        'search_query': query,
        'user_liked_ids': user_liked_ids,
    }
    return render(request, 'gallery/feed.html', context)


@login_required
def upload_artwork(request):
    """Upload new artwork"""
    if request.method == 'POST':
        form = ArtworkForm(request.POST, request.FILES)
        if form.is_valid():
            artwork = form.save(commit=False)
            artwork.artist = request.user

            image_file = request.FILES.get('image')
            if image_file:
                # Check if using local storage
                if getattr(django_settings, 'USE_LOCAL_STORAGE', False):
                    # Local file storage
                    artwork.image_file = image_file
                    artwork.image = ''  # Clear URL field
                else:
                    # Supabase storage
                    if supabase:
                        try:
                            # Define a unique path for the image in the bucket
                            file_path = f"artworks/{request.user.username}/{image_file.name}"
                            
                            # Upload to Supabase Storage
                            supabase.storage.from_("artworks").upload(
                                file_path, 
                                image_file.read(), 
                                {"content-type": image_file.content_type}
                            )
                            
                            # Get the public URL
                            public_url = supabase.storage.from_("artworks").get_public_url(file_path)
                            artwork.image = public_url

                        except Exception as e:
                            logger.error(f"Supabase upload failed: {e}")
                            messages.error(request, f"Error uploading image: {str(e)}")
                            return render(request, 'gallery/upload.html', {'form': form})
                    else:
                        # Fallback to local if Supabase not available
                        artwork.image_file = image_file
                        artwork.image = ''

            artwork.save()
            
            # Process tags
            tags_input = form.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    artwork.tags.add(tag)
            
            # Award XP for uploading (+25 XP)
            leveled_up, new_level = request.user.award_xp(25)
            
            # Store XP gain info in session for toast notification
            request.session['xp_gained'] = 25
            request.session['xp_action'] = 'uploading artwork'
            if leveled_up:
                request.session['level_up'] = new_level
            
            messages.success(request, "Your artwork has been uploaded successfully!")
            return redirect('detail', pk=artwork.pk)
        else:
            # Pass form errors to the template
            return render(request, 'gallery/upload.html', {'form': form})
    else:
        form = ArtworkForm()
    return render(request, 'gallery/upload.html', {'form': form})


def artwork_detail(request, pk):
    """Display individual artwork"""
    artwork = get_object_or_404(
        Artwork.objects.select_related('artist').prefetch_related('tags', 'likes', 'comments__user'),
        pk=pk
    )
    
    # Check if current user has liked this artwork
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = artwork.likes.filter(user=request.user).exists()
    
    # Get comments
    comments = artwork.comments.all()
    
    # Comment form for authenticated users
    comment_form = CommentForm() if request.user.is_authenticated else None
    
    # Check if user is the owner (for delete button)
    is_owner = request.user.is_authenticated and request.user == artwork.artist
    
    # Mark comments as read if owner is viewing
    if is_owner:
        # Mark all unread comments (not by owner) as read
        artwork.comments.filter(is_read=False).exclude(user=request.user).update(is_read=True)
    
    context = {
        'artwork': artwork,
        'user_has_liked': user_has_liked,
        'comments': comments,
        'comment_form': comment_form,
        'is_owner': is_owner,
    }
    return render(request, 'gallery/detail.html', context)


@login_required
def delete_artwork(request, pk):
    """Delete an artwork (owner only)"""
    artwork = get_object_or_404(Artwork, pk=pk)
    
    # Verify ownership
    if artwork.artist != request.user:
        messages.error(request, "You can only delete your own artwork.")
        return redirect('detail', pk=pk)
    
    if request.method == 'POST':
        # Delete from storage if using Supabase
        if artwork.image and supabase and not getattr(django_settings, 'USE_LOCAL_STORAGE', False):
            try:
                # Extract file path from URL
                file_path = f"artworks/{request.user.username}/" + artwork.image.split('/')[-1]
                supabase.storage.from_("artworks").remove([file_path])
            except Exception as e:
                logger.warning(f"Could not delete from Supabase: {e}")
        
        # Delete local file if exists
        if artwork.image_file:
            try:
                if os.path.exists(artwork.image_file.path):
                    os.remove(artwork.image_file.path)
            except Exception as e:
                logger.warning(f"Could not delete local file: {e}")
        
        artwork_title = artwork.title
        artwork.delete()
        messages.success(request, f'"{artwork_title}" has been deleted.')
        return redirect('profile', username=request.user.username)
    
    # GET request - show confirmation
    return render(request, 'gallery/delete_confirm.html', {'artwork': artwork})


@login_required
def edit_artwork(request, pk):
    """Edit an artwork (owner only) - title, description, tags only"""
    artwork = get_object_or_404(Artwork, pk=pk)
    
    # Verify ownership
    if artwork.artist != request.user:
        messages.error(request, "You can only edit your own artwork.")
        return redirect('detail', pk=pk)
    
    if request.method == 'POST':
        form = ArtworkEditForm(request.POST, instance=artwork)
        if form.is_valid():
            form.save()
            
            # Handle tags
            tags_input = form.cleaned_data.get('tags_input', '')
            artwork.tags.clear()
            if tags_input:
                tag_names = [t.strip().lower() for t in tags_input.split(',') if t.strip()]
                for tag_name in tag_names:
                    tag, _ = Tag.objects.get_or_create(
                        name=tag_name,
                        defaults={'slug': tag_name.replace(' ', '-')}
                    )
                    artwork.tags.add(tag)
            
            # No XP for edits (prevent XP farming)
            messages.success(request, "Your artwork has been updated!")
            return redirect('detail', pk=pk)
    else:
        # Pre-fill tags
        current_tags = ', '.join([tag.name for tag in artwork.tags.all()])
        form = ArtworkEditForm(instance=artwork, initial={'tags_input': current_tags})
    
    return render(request, 'gallery/edit.html', {'form': form, 'artwork': artwork})
