from django.core.management.base import BaseCommand
from django.utils.text import slugify
from products.models import Category


class Command(BaseCommand):
    help = 'Setup initial category hierarchy'

    def handle(self, *args, **options):
        # Create sample category hierarchy
        categories_data = {
            'All Products': {
                'Bakery': {
                    'Bread': {},
                    'Cookies': {},
                    'Pastries': {}
                },
                'Produce': {
                    'Fruits': {
                        'Citrus': {},
                        'Berries': {},
                        'Tropical': {}
                    },
                    'Vegetables': {
                        'Leafy Greens': {},
                        'Root Vegetables': {},
                        'Herbs': {}
                    }
                },
                'Electronics': {
                    'Mobile Phones': {},
                    'Computers': {
                        'Laptops': {},
                        'Desktops': {},
                        'Accessories': {}
                    },
                    'Audio': {
                        'Headphones': {},
                        'Speakers': {},
                        'Microphones': {}
                    }
                }
            }
        }

        def create_categories(data, parent=None):
            for name, children in data.items():
                slug = slugify(name)
                category, created = Category.objects.get_or_create(
                    name=name,
                    slug=slug,
                    defaults={'parent': parent}
                )

                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Created category: {category.get_full_path()}')
                    )

                if children:
                    create_categories(children, category)

        create_categories(categories_data)
        self.stdout.write(self.style.SUCCESS('Category hierarchy setup complete!'))
