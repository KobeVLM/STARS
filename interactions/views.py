import re
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from gallery.models import Artwork
from users.models import Notification, SuspensionAppeal
from .models import Like, Comment, Report, CommentFlag
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
        
        # Award XP to the artwork artist for receiving a like (+1 XP)
        if artwork.artist != request.user:
            leveled_up, new_level = artwork.artist.award_xp(1)
            # Award XP to the user for giving a like (+1 XP)
            request.user.award_xp(1)
    
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
    
    # Check if user is suspended
    if request.user.suspension_end_date and request.user.suspension_end_date > timezone.now():
        remaining = request.user.suspension_end_date - timezone.now()
        hours = int(remaining.total_seconds() // 3600) + 1
        messages.error(request, f"You are currently suspended from commenting. Try again in {hours} hours.")
        return redirect('detail', pk=artwork_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data.get('content', '')
            
            # Check for external links
            if re.search(r'http[s]?://|www\.', content):
                messages.error(request, "Your comment contains an external link, which is not allowed. Please remove it and try again.")
                return redirect('detail', pk=artwork_id)
                
            # Check for banned words
            banned_words = ['badword', 'profanity', 'spam'] # Simplified list for demo
            content_lower = content.lower()
            if any(word in content_lower for word in banned_words):
                messages.error(request, "Your comment contains inappropriate language and was blocked.")
                return redirect('detail', pk=artwork_id)

            comment = form.save(commit=False)
            comment.user = request.user
            comment.artwork = artwork
            comment.save()
            
            # XP Gamification
            request.user.award_xp(2) # Posting a comment
            if artwork.artist != request.user:
                artwork.artist.award_xp(2) # Receiving a comment
            
            messages.success(request, 'Comment posted! (+2 XP)')
    
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


@login_required
def report_comment(request, comment_id):
    """Flag a comment. 3 flags = 24h suspension."""
    comment = get_object_or_404(Comment, pk=comment_id)
    artwork_id = comment.artwork.id
    
    if comment.user == request.user:
        messages.error(request, "You cannot report your own comment.")
        return redirect('detail', pk=artwork_id)
        
    flag, created = CommentFlag.objects.get_or_create(comment=comment, flagged_by=request.user)
    
    if created:
        messages.success(request, "Comment flagged for review.")
        flag_count = comment.flags.count()
        if flag_count >= 3 and (not comment.user.suspension_end_date or comment.user.suspension_end_date < timezone.now()):
            comment.user.suspension_end_date = timezone.now() + timedelta(hours=24)
            comment.user.save()
            
            Notification.objects.create(
                user=comment.user,
                message="You have been suspended from commenting for 24 hours due to multiple community flags on your comment.",
                action_link="/interactions/appeal/",
                action_text="Dispute this flag"
            )
    else:
        messages.info(request, "You have already flagged this comment.")
        
    return redirect('detail', pk=artwork_id)


@login_required
def appeal_suspension(request):
    """Allow a suspended user to appeal"""
    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason:
            SuspensionAppeal.objects.create(user=request.user, reason=reason)
            messages.success(request, "Your appeal has been submitted to the admin team.")
        return redirect('feed')
    return render(request, 'interactions/appeal_form.html')


@login_required
def pin_comment(request, comment_id):
    """Pin or unpin a comment. Only artwork owner can do this."""
    comment = get_object_or_404(Comment, pk=comment_id)
    artwork_id = comment.artwork.id
    
    if request.user != comment.artwork.artist:
        messages.error(request, "Only the artwork owner can pin comments.")
        return redirect('detail', pk=artwork_id)
        
    comment.is_pinned = not comment.is_pinned
    comment.save()
    
    if comment.is_pinned:
        messages.success(request, "Comment pinned!")
        if comment.user != request.user:
            comment.user.mentor_points += 10
            comment.user.save()
            Notification.objects.create(
                user=comment.user,
                message=f"Your comment on '{comment.artwork.title}' was pinned! You earned 10 Mentor Points."
            )
    else:
        messages.success(request, "Comment unpinned.")
        
    return redirect('detail', pk=artwork_id)
