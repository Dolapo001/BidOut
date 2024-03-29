from django.core.management.base import BaseCommand
from auctions.models import Category

class Command(BaseCommand):
    help = 'Populates the predefined categories'

    def handle(self, *args, **options):
        # Define the predefined categories
        categories = [
            'Fashion',
            'Electronics',
            'Autos',
            'Toys',
            'Music',
            'Plants',
            'Cards',
            # Add more categories as needed
        ]

        excluded_categories = ['ToysMusicPlantsCards']

        # Create categories
        for category_name in categories:
            if category_name not in excluded_categories:
                Category.objects.get_or_create(name=category_name)

        self.stdout.write(self.style.SUCCESS('Categories populated successfully.'))
