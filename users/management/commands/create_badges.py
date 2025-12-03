from django.core.management.base import BaseCommand
from users.models import Badge


class Command(BaseCommand):
    help = 'Create initial badge set for STARS platform'

    def handle(self, *args, **kwargs):
        badges = [
            {
                'name': 'First Upload',
                'description': 'Upload your first artwork',
                'icon': '🎨',
                'criteria_type': 'uploads',
                'criteria_value': 1,
            },
            {
                'name': 'Prolific Artist',
                'description': 'Upload 10 artworks',
                'icon': '🖼️',
                'criteria_type': 'uploads',
                'criteria_value': 10,
            },
            {
                'name': 'Master Creator',
                'description': 'Upload 25 artworks',
                'icon': '🎭',
                'criteria_type': 'uploads',
                'criteria_value': 25,
            },
            {
                'name': 'Social Butterfly',
                'description': 'Give 50 likes to other artworks',
                'icon': '💬',
                'criteria_type': 'likes_given',
                'criteria_value': 50,
            },
            {
                'name': 'Art Enthusiast',
                'description': 'Give 100 likes to other artworks',
                'icon': '❤️',
                'criteria_type': 'likes_given',
                'criteria_value': 100,
            },
            {
                'name': 'Popular',
                'description': 'Receive 100 likes on your artworks',
                'icon': '🌟',
                'criteria_type': 'likes_received',
                'criteria_value': 100,
            },
            {
                'name': 'Superstar',
                'description': 'Receive 500 likes on your artworks',
                'icon': '⭐',
                'criteria_type': 'likes_received',
                'criteria_value': 500,
            },
            {
                'name': 'Rising Star',
                'description': 'Reach level 5',
                'icon': '✨',
                'criteria_type': 'level',
                'criteria_value': 5,
            },
            {
                'name': 'Master Artist',
                'description': 'Reach level 10',
                'icon': '👑',
                'criteria_type': 'level',
                'criteria_value': 10,
            },
            {
                'name': 'Legendary',
                'description': 'Reach level 20',
                'icon': '🏆',
                'criteria_type': 'level',
                'criteria_value': 20,
            },
            {
                'name': 'Commenter',
                'description': 'Post 10 comments',
                'icon': '💭',
                'criteria_type': 'comments',
                'criteria_value': 10,
            },
            {
                'name': 'Conversationalist',
                'description': 'Post 50 comments',
                'icon': '💬',
                'criteria_type': 'comments',
                'criteria_value': 50,
            },
        ]

        created_count = 0
        for badge_data in badges:
            badge, created = Badge.objects.get_or_create(
                name=badge_data['name'],
                defaults=badge_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created badge: {badge.icon} {badge.name}')
                )
            else:
                self.stdout.write(f'Badge already exists: {badge.icon} {badge.name}')

        self.stdout.write(
            self.style.SUCCESS(f'\nSuccessfully created {created_count} new badges!')
        )
