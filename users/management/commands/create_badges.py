"""Management command to create default badges"""
from django.core.management.base import BaseCommand
from users.models import Badge


class Command(BaseCommand):
    help = 'Create or update default badges for STARS platform'

    def handle(self, *args, **kwargs):
        badges = [
            # Upload-based badges
            {'name': 'First Upload', 'description': 'Upload your first artwork', 'icon': '🎨', 'criteria_type': 'uploads', 'criteria_value': 1, 'xp_reward': 25},
            {'name': 'Art Enthusiast', 'description': 'Upload 5 artworks', 'icon': '🖼️', 'criteria_type': 'uploads', 'criteria_value': 5, 'xp_reward': 50},
            {'name': 'Prolific Artist', 'description': 'Upload 10 artworks', 'icon': '🎭', 'criteria_type': 'uploads', 'criteria_value': 10, 'xp_reward': 100},
            {'name': 'Gallery Master', 'description': 'Upload 25 artworks', 'icon': '🏛️', 'criteria_type': 'uploads', 'criteria_value': 25, 'xp_reward': 200},
            {'name': 'Legend', 'description': 'Upload 50 artworks', 'icon': '👑', 'criteria_type': 'uploads', 'criteria_value': 50, 'xp_reward': 500},
            
            # Likes received badges
            {'name': 'Appreciated', 'description': 'Receive 5 likes on your artworks', 'icon': '💕', 'criteria_type': 'likes_received', 'criteria_value': 5, 'xp_reward': 25},
            {'name': 'Popular', 'description': 'Receive 25 likes on your artworks', 'icon': '⭐', 'criteria_type': 'likes_received', 'criteria_value': 25, 'xp_reward': 75},
            {'name': 'Rising Star', 'description': 'Receive 50 likes on your artworks', 'icon': '🌟', 'criteria_type': 'likes_received', 'criteria_value': 50, 'xp_reward': 150},
            {'name': 'Superstar', 'description': 'Receive 100 likes on your artworks', 'icon': '💫', 'criteria_type': 'likes_received', 'criteria_value': 100, 'xp_reward': 300},
            
            # Likes given badges (engagement)
            {'name': 'Supporter', 'description': 'Like 10 artworks', 'icon': '👏', 'criteria_type': 'likes_given', 'criteria_value': 10, 'xp_reward': 25},
            {'name': 'Art Lover', 'description': 'Like 50 artworks', 'icon': '❤️', 'criteria_type': 'likes_given', 'criteria_value': 50, 'xp_reward': 75},
            {'name': 'Curator', 'description': 'Like 100 artworks', 'icon': '🎯', 'criteria_type': 'likes_given', 'criteria_value': 100, 'xp_reward': 150},
            
            # Comment badges
            {'name': 'Conversationalist', 'description': 'Write 5 comments', 'icon': '💬', 'criteria_type': 'comments', 'criteria_value': 5, 'xp_reward': 25},
            {'name': 'Critic', 'description': 'Write 25 comments', 'icon': '📝', 'criteria_type': 'comments', 'criteria_value': 25, 'xp_reward': 75},
            {'name': 'Mentor', 'description': 'Write 50 comments', 'icon': '🎓', 'criteria_type': 'comments', 'criteria_value': 50, 'xp_reward': 150},
            
            # Level badges
            {'name': 'Level 5', 'description': 'Reach level 5', 'icon': '🔰', 'criteria_type': 'level', 'criteria_value': 5, 'xp_reward': 50},
            {'name': 'Level 10', 'description': 'Reach level 10', 'icon': '🏅', 'criteria_type': 'level', 'criteria_value': 10, 'xp_reward': 100},
            {'name': 'Level 25', 'description': 'Reach level 25', 'icon': '🥇', 'criteria_type': 'level', 'criteria_value': 25, 'xp_reward': 250},
            {'name': 'Level 50', 'description': 'Reach level 50', 'icon': '🏆', 'criteria_type': 'level', 'criteria_value': 50, 'xp_reward': 500},
            
            # Follower badges
            {'name': 'Friendly', 'description': 'Gain 5 followers', 'icon': '🤝', 'criteria_type': 'followers', 'criteria_value': 5, 'xp_reward': 50},
            {'name': 'Social Butterfly', 'description': 'Gain 25 followers', 'icon': '🦋', 'criteria_type': 'followers', 'criteria_value': 25, 'xp_reward': 150},
            {'name': 'Influencer', 'description': 'Gain 50 followers', 'icon': '🌐', 'criteria_type': 'followers', 'criteria_value': 50, 'xp_reward': 300},
        ]
        
        created_count = 0
        updated_count = 0
        
        for badge_data in badges:
            badge, created = Badge.objects.update_or_create(
                name=badge_data['name'],
                defaults=badge_data
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"  ✓ Created: {badge.icon} {badge.name}"))
            else:
                updated_count += 1
                self.stdout.write(f"  • Updated: {badge.icon} {badge.name}")
        
        self.stdout.write(self.style.SUCCESS(f"\nDone! Created: {created_count}, Updated: {updated_count}"))
