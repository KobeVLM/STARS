from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q
from django.utils import timezone
from users.models import CustomUser, Badge, SuspensionAppeal, Notification
from gallery.models import Artwork
from interactions.models import Like, Comment, Report, CommentFlag


@staff_member_required
def admin_dashboard(request):
    """Admin dashboard with platform statistics"""
    stats = {
        'total_users': CustomUser.objects.count(),
        'total_artworks': Artwork.objects.count(),
        'total_likes': Like.objects.count(),
        'total_comments': Comment.objects.count(),
        'active_users': CustomUser.objects.filter(is_active=True).count(),
        'staff_users': CustomUser.objects.filter(is_staff=True).count(),
    }
    
    # Recent users
    recent_users = CustomUser.objects.order_by('-date_joined')[:5]
    
    # Top users by XP
    top_users = CustomUser.objects.order_by('-xp')[:5]
    
    # Pending appeals and flags count
    pending_appeals_count = SuspensionAppeal.objects.filter(status='pending').count()
    flags_count = CommentFlag.objects.count()

    context = {
        'stats': stats,
        'recent_users': recent_users,
        'top_users': top_users,
        'pending_appeals_count': pending_appeals_count,
        'flags_count': flags_count,
    }
    return render(request, 'core/admin_dashboard.html', context)


@staff_member_required
def admin_users(request):
    """Admin user management - list all users"""
    # Get search query
    search_query = request.GET.get('q', '')
    
    # Get filter parameters
    status_filter = request.GET.get('status', 'all')
    role_filter = request.GET.get('role', 'all')
    
    # Base queryset
    users = CustomUser.objects.annotate(
        artwork_count=Count('artworks'),
        comment_count=Count('comments'),
        like_count=Count('like')  # Based on error message, the field is 'like'
    ).order_by('-date_joined')
    
    # Apply search
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) | 
            Q(email__icontains=search_query)
        )
    
    # Apply status filter
    if status_filter == 'active':
        users = users.filter(is_active=True)
    elif status_filter == 'inactive':
        users = users.filter(is_active=False)
    
    # Apply role filter
    if role_filter == 'staff':
        users = users.filter(is_staff=True)
    elif role_filter == 'regular':
        users = users.filter(is_staff=False)
    
    context = {
        'users': users,
        'search_query': search_query,
        'status_filter': status_filter,
        'role_filter': role_filter,
    }
    return render(request, 'core/admin_users.html', context)


@staff_member_required
def admin_user_edit(request, user_id):
    """Admin user edit - modify user details"""
    user_to_edit = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'toggle_active':
            # Prevent self-deactivation
            if user_to_edit == request.user and user_to_edit.is_active:
                messages.error(request, 'You cannot deactivate your own account.')
            else:
                user_to_edit.is_active = not user_to_edit.is_active
                user_to_edit.save()
                status = 'activated' if user_to_edit.is_active else 'deactivated'
                messages.success(request, f'User {user_to_edit.username} has been {status}.')
        
        elif action == 'toggle_staff':
            # Prevent self-demotion
            if user_to_edit == request.user and user_to_edit.is_staff:
                messages.error(request, 'You cannot revoke your own staff privileges.')
            else:
                user_to_edit.is_staff = not user_to_edit.is_staff
                user_to_edit.save()
                status = 'granted' if user_to_edit.is_staff else 'revoked'
                messages.success(request, f'Staff privileges {status} for {user_to_edit.username}.')
        
        elif action == 'adjust_xp':
            xp_change = int(request.POST.get('xp_amount', 0))
            if xp_change != 0:
                user_to_edit.award_xp(xp_change)
                messages.success(request, f'Adjusted XP by {xp_change:+d} for {user_to_edit.username}.')
        
        elif action == 'update_bio':
            new_bio = request.POST.get('bio', '')
            user_to_edit.bio = new_bio
            user_to_edit.save()
            messages.success(request, f'Updated bio for {user_to_edit.username}.')
        
        return redirect('admin_user_edit', user_id=user_id)
    
    # Get user stats
    user_stats = {
        'artworks': user_to_edit.artworks.count(),
        'comments': user_to_edit.comments.count(),
        'likes_given': Like.objects.filter(user=user_to_edit).count(),  # Direct query instead of reverse relation
        'likes_received': Like.objects.filter(artwork__artist=user_to_edit).count(),
        'badges': user_to_edit.earned_badges.count(),
    }
    
    context = {
        'user_to_edit': user_to_edit,
        'user_stats': user_stats,
    }
    return render(request, 'core/admin_user_edit.html', context)


@staff_member_required
def admin_reports(request):
    """Admin view for content moderation - review reported artworks"""
    status_filter = request.GET.get('status', 'pending')
    
    reports = Report.objects.select_related('reporter', 'artwork', 'artwork__artist', 'resolved_by')
    
    if status_filter == 'pending':
        reports = reports.filter(status='pending')
    elif status_filter == 'reviewed':
        reports = reports.filter(status='reviewed')
    elif status_filter == 'resolved':
        reports = reports.filter(status__in=['dismissed', 'resolved'])
    # 'all' shows everything
    
    # Count pending reports for badge
    pending_count = Report.objects.filter(status='pending').count()
    
    context = {
        'reports': reports,
        'status_filter': status_filter,
        'pending_count': pending_count,
    }
    return render(request, 'core/admin_reports.html', context)


@staff_member_required
def admin_report_action(request, report_id):
    """Handle admin action on a report"""
    report = get_object_or_404(Report, pk=report_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        admin_notes = request.POST.get('admin_notes', '')
        
        if action == 'dismiss':
            report.status = 'dismissed'
            report.admin_notes = admin_notes
            report.resolved_at = timezone.now()
            report.resolved_by = request.user
            report.save()
            messages.success(request, f'Report dismissed.')
        
        elif action == 'warn':
            report.status = 'resolved'
            report.admin_notes = admin_notes
            report.resolved_at = timezone.now()
            report.resolved_by = request.user
            report.save()
            messages.success(request, f'Report resolved. Consider messaging the artist about the issue.')
        
        elif action == 'delete_artwork':
            artwork_title = report.artwork.title
            artwork = report.artwork  # Store reference before deleting
            # Save backup info BEFORE deleting
            report.artwork_title_backup = artwork_title
            report.status = 'resolved'
            report.admin_notes = f"Artwork deleted by admin. {admin_notes}"
            report.resolved_at = timezone.now()
            report.resolved_by = request.user
            report.save()
            # Now delete the artwork (report stays because we saved it first, and artwork is SET_NULL)
            artwork.delete()
            messages.success(request, f'Artwork "{artwork_title}" has been deleted.')
        
        elif action == 'review':
            report.status = 'reviewed'
            report.admin_notes = admin_notes
            report.save()
            messages.info(request, f'Report marked as under review.')
    
    return redirect('admin_reports')


@staff_member_required
def admin_badges(request):
    """Admin badge management - list, create, edit badges"""
    badges = Badge.objects.annotate(
        users_count=Count('users')
    ).order_by('criteria_type', 'criteria_value')
    
    # Handle form submission for creating new badge
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'create':
            name = request.POST.get('name', '').strip()
            description = request.POST.get('description', '').strip()
            icon = request.POST.get('icon', '🏆').strip() or '🏆'
            criteria_type = request.POST.get('criteria_type')
            criteria_value = request.POST.get('criteria_value', 1)
            xp_reward = request.POST.get('xp_reward', 50)
            
            if name and description and criteria_type:
                try:
                    Badge.objects.create(
                        name=name,
                        description=description,
                        icon=icon,
                        criteria_type=criteria_type,
                        criteria_value=int(criteria_value),
                        xp_reward=int(xp_reward)
                    )
                    messages.success(request, f'Badge "{name}" created successfully!')
                except Exception as e:
                    messages.error(request, f'Error creating badge: {str(e)}')
            else:
                messages.error(request, 'Please fill in all required fields.')
            return redirect('admin_badges')
    
    # Get criteria type choices
    criteria_choices = Badge._meta.get_field('criteria_type').choices
    
    context = {
        'badges': badges,
        'criteria_choices': criteria_choices,
    }
    return render(request, 'core/admin_badges.html', context)


@staff_member_required
def admin_badge_action(request, badge_id):
    """Handle badge edit/delete actions"""
    badge = get_object_or_404(Badge, id=badge_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'delete':
            badge_name = badge.name
            badge.delete()
            messages.success(request, f'Badge "{badge_name}" deleted.')
            return redirect('admin_badges')
        
        elif action == 'update':
            badge.name = request.POST.get('name', badge.name).strip()
            badge.description = request.POST.get('description', badge.description).strip()
            badge.icon = request.POST.get('icon', badge.icon).strip() or '🏆'
            badge.criteria_type = request.POST.get('criteria_type', badge.criteria_type)
            badge.criteria_value = int(request.POST.get('criteria_value', badge.criteria_value))
            badge.xp_reward = int(request.POST.get('xp_reward', badge.xp_reward))
            badge.save()
            messages.success(request, f'Badge "{badge.name}" updated.')
            return redirect('admin_badges')
    
    return redirect('admin_badges')


@staff_member_required
def admin_disputes(request):
    """Admin view for suspension appeals"""
    status_filter = request.GET.get('status', 'pending')
    
    appeals = SuspensionAppeal.objects.select_related('user')
    
    if status_filter == 'pending':
        appeals = appeals.filter(status='pending')
    elif status_filter == 'approved':
        appeals = appeals.filter(status='approved')
    elif status_filter == 'denied':
        appeals = appeals.filter(status='denied')
        
    pending_count = SuspensionAppeal.objects.filter(status='pending').count()
    
    context = {
        'appeals': appeals,
        'status_filter': status_filter,
        'pending_count': pending_count,
    }
    return render(request, 'core/admin_disputes.html', context)


@staff_member_required
def admin_dispute_action(request, appeal_id):
    """Handle admin action on a dispute"""
    appeal = get_object_or_404(SuspensionAppeal, pk=appeal_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            appeal.status = 'approved'
            appeal.save()
            # Lift the user's suspension
            appeal.user.suspension_end_date = None
            appeal.user.save()
            
            # Send Notification
            Notification.objects.create(
                user=appeal.user,
                message="Your suspension appeal has been approved! Your commenting privileges have been restored."
            )
            messages.success(request, f'Appeal approved for {appeal.user.username}.')
            
        elif action == 'deny':
            appeal.status = 'denied'
            appeal.save()
            
            # Send Notification
            Notification.objects.create(
                user=appeal.user,
                message="Your suspension appeal has been denied by the moderation team."
            )
            messages.warning(request, f'Appeal denied for {appeal.user.username}.')
            
    return redirect('admin_disputes')


@staff_member_required
def admin_flags(request):
    """Admin view for comment flags"""
    # Get all flags with their related comments and users
    flags = CommentFlag.objects.select_related('comment', 'comment__user', 'flagged_by')
    
    context = {
        'flags': flags,
    }
    return render(request, 'core/admin_flags.html', context)


@staff_member_required
def admin_flag_action(request, flag_id):
    """Handle admin action on a comment flag"""
    flag = get_object_or_404(CommentFlag, pk=flag_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'dismiss':
            flag.delete()
            messages.success(request, 'Flag has been dismissed.')
            
        elif action == 'delete_comment':
            # Delete the offending comment (this will cascade delete the flag)
            comment_content = flag.comment.content
            comment_author = flag.comment.user.username
            flag.comment.delete()
            messages.success(request, f'Comment by {comment_author} has been deleted.')
            
    return redirect('admin_flags')
