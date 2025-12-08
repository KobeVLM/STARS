from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from gallery.models import Artwork
from .models import Like, Comment
from .forms import CommentForm


@login_required
def toggle_like(request, artwork_id):
    """Toggle like on artwork (AJAX endpoint)"""
    artwork = get_object_or_404(Artwork, pk=artwork_id)
    
    like, created = Like.objects.get_or_create(user=request.user, artwork=artwork)
    
    if not created:
        # Unlike - remove the like
        like.delete()
        liked = False
        like_count = artwork.likes.count()
    else:
        # Liked
        liked = True
        like_count = artwork.likes.count()
    
    # Return JSON for AJAX or redirect for regular requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'like_count': like_count
        })
    else:
        return redirect('detail', pk=artwork_id)


@login_required
def add_comment(request, artwork_id):
    """Add a comment to an artwork"""
    artwork = get_object_or_404(Artwork, pk=artwork_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.artwork = artwork
            comment.save()
            
            # Award XP for commenting (+5 XP)
            leveled_up = request.user.award_xp(5)
            if leveled_up:
                messages.success(request, f'Comment posted! (+5 XP). Level Up! You are now level {request.user.level}', extra_tags='level_up')
            else:
                messages.success(request, 'Comment posted! (+5 XP)')
    
    return redirect('detail', pk=artwork_id)


@login_required
def delete_comment(request, comment_id):
    """Delete a comment (only by the comment author)"""
    comment = get_object_or_404(Comment, pk=comment_id)
    artwork_id = comment.artwork.id
    
    # Check if user owns the comment
    if comment.user == request.user:
        comment.delete()
        messages.success(request, 'Comment deleted.')
    else:
        messages.error(request, 'You can only delete your own comments.')
    
    return redirect('detail', pk=artwork_id)
