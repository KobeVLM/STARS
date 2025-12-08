from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Artwork, Tag
from .forms import ArtworkForm
from interactions.forms import CommentForm


def explore_feed(request):
    """Main gallery feed with search and filtering"""
    artworks = Artwork.objects.all().select_related('artist').prefetch_related('tags', 'likes')
    
    # Search by title or artist username
    query = request.GET.get('q')
    if query:
        artworks = artworks.filter(
            Q(title__icontains=query) | Q(artist__username__icontains=query)
        )
    
    # Filter by tag
    tag_slug = request.GET.get('tag')
    if tag_slug:
        artworks = artworks.filter(tags__slug=tag_slug)

    context = {
        'artworks': artworks,
        'tags': Tag.objects.all(),
        'current_tag': tag_slug,
        'search_query': query,
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
            artwork.save()
            
            # Process tags
            tags_input = form.cleaned_data.get('tags_input', '')
            if tags_input:
                tag_names = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    artwork.tags.add(tag)
            
            # Award XP for upload (50 XP)
            leveled_up = request.user.award_xp(50)
            if leveled_up:
                messages.success(request, f"Artwork uploaded! (+50 XP). Level Up! You are now level {request.user.level}", extra_tags='level_up')
            else:
                messages.success(request, 'Artwork uploaded! (+50 XP)')
            
            return redirect('detail', pk=artwork.pk)
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
    
    context = {
        'artwork': artwork,
        'user_has_liked': user_has_liked,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'gallery/detail.html', context)
