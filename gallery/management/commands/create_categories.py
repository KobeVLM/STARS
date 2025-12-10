from django.core.management.base import BaseCommand
from gallery.models import Category


class Command(BaseCommand):
    help = 'Creates default artwork categories'

    def handle(self, *args, **options):
        categories = [
            {'name': 'Digital Art', 'icon': '🖥️', 'order': 1},
            {'name': 'Traditional', 'icon': '🎨', 'order': 2},
            {'name': 'Photography', 'icon': '📷', 'order': 3},
            {'name': 'Fan Art', 'icon': '⭐', 'order': 4},
            {'name': 'Original Character', 'icon': '🧑‍🎤', 'order': 5},
            {'name': 'Illustration', 'icon': '✏️', 'order': 6},
            {'name': 'Graphic Design', 'icon': '🎯', 'order': 7},
            {'name': 'Other', 'icon': '📁', 'order': 99},
        ]
        
        created_count = 0
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'icon': cat_data['icon'], 'order': cat_data['order']}
            )
            if created:
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f"Created category: {category}"))
            else:
                self.stdout.write(f"Category already exists: {category}")
        
        self.stdout.write(self.style.SUCCESS(f"\n✅ Done! Created {created_count} new categories."))
