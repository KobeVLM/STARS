from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from gallery.models import Artwork
from .models import Like, Comment, Report
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
        # Liked - award XP to artwork owner (not to self)
        liked = True
        like_count = artwork.likes.count()
        
        # Award XP to the artwork artist for receiving a like (+5 XP)
        if artwork.artist != request.user:
            leveled_up, new_level = artwork.artist.award_xp(5)
            # Note: We can't show toast to the artwork owner in real-time
            # but they'll see their XP increase next time they visit
    
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
            
            messages.success(request, 'Comment posted!')
    
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


@login_required
def report_artwork(request, artwork_id):
    """Report an artwork for content moderation"""
    artwork = get_object_or_404(Artwork, pk=artwork_id)
    
    # Can't report your own artwork
    if artwork.artist == request.user:
        messages.error(request, "You cannot report your own artwork.")
        return redirect('detail', pk=artwork_id)
    
    # Check if user already reported this artwork
    existing_report = Report.objects.filter(
        reporter=request.user, 
        artwork=artwork,
        status__in=['pending', 'reviewed']
    ).exists()
    
    if existing_report:
        messages.info(request, "You have already reported this artwork. Our team is reviewing it.")
        return redirect('detail', pk=artwork_id)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        description = request.POST.get('description', '')
        
        if reason:
            Report.objects.create(
                reporter=request.user,
                artwork=artwork,
                reason=reason,
                description=description
            )
            messages.success(request, "Thank you for your report. Our team will review it shortly.")
            return redirect('detail', pk=artwork_id)
        else:
            messages.error(request, "Please select a reason for your report.")
    
    # Show report form
    return render(request, 'interactions/report_form.html', {'artwork': artwork})
