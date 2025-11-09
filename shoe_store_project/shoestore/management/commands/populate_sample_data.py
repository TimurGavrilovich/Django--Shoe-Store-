from django.core.management.base import BaseCommand
from shoestore.models import Category, Brand, Product, ProductSize

class Command(BaseCommand):
    help = 'Populate database with sample shoe data'

    def handle(self, *args, **options):
        # Create categories
        categories = [
            {'name': 'Sneakers', 'slug': 'sneakers'},
            {'name': 'Running', 'slug': 'running'},
            {'name': 'Casual', 'slug': 'casual'},
            {'name': 'Formal', 'slug': 'formal'},
            {'name': 'Boots', 'slug': 'boots'},
        ]
        
        for cat_data in categories:
            Category.objects.get_or_create(**cat_data)
        
        # Create brands
        brands = ['Nike', 'Adidas', 'Puma', 'New Balance', 'Vans', 'Converse']
        for brand_name in brands:
            Brand.objects.get_or_create(name=brand_name)
        
        # Sample products data
        products_data = [
            {
                'name': 'Nike Air Max 270',
                'slug': 'nike-air-max-270',
                'description': 'The Nike Air Max 270 delivers comfortable style and incredible energy return.',
                'price': 150.00,
                'discount_price': 129.99,
                'category': 'Sneakers',
                'brand': 'Nike',
                'gender': 'U',
                'featured': True,
            },
            {
                'name': 'Adidas Ultraboost 21',
                'slug': 'adidas-ultraboost-21',
                'description': 'Experience incredible energy return and comfort with Adidas Ultraboost.',
                'price': 180.00,
                'category': 'Running',
                'brand': 'Adidas',
                'gender': 'U',
                'featured': True,
            },
            {
                'name': 'Puma RS-X',
                'slug': 'puma-rs-x',
                'description': 'Bold designs and comfortable fit with Puma RS-X sneakers.',
                'price': 110.00,
                'category': 'Sneakers',
                'brand': 'Puma',
                'gender': 'U',
                'featured': True,
            },
            {
                'name': 'New Balance 574',
                'slug': 'new-balance-574',
                'description': 'Classic style meets modern comfort with New Balance 574.',
                'price': 89.99,
                'category': 'Casual',
                'brand': 'New Balance',
                'gender': 'U',
                'featured': False,
            },
            {
                'name': 'Vans Old Skool',
                'slug': 'vans-old-skool',
                'description': 'The iconic Vans Old Skool with timeless style and durability.',
                'price': 65.00,
                'category': 'Casual',
                'brand': 'Vans',
                'gender': 'U',
                'featured': True,
            },
            {
                'name': 'Converse Chuck Taylor',
                'slug': 'converse-chuck-taylor',
                'description': 'The classic Converse Chuck Taylor All Star sneakers.',
                'price': 55.00,
                'discount_price': 45.00,
                'category': 'Casual',
                'brand': 'Converse',
                'gender': 'U',
                'featured': False,
            },
            {
                'name': 'Nike Air Force 1',
                'slug': 'nike-air-force-1',
                'description': 'The classic Nike Air Force 1 in white with premium leather.',
                'price': 100.00,
                'category': 'Sneakers',
                'brand': 'Nike',
                'gender': 'U',
                'featured': True,
            },
            {
                'name': 'Adidas Stan Smith',
                'slug': 'adidas-stan-smith',
                'description': 'Clean, minimalist design with the iconic Adidas Stan Smith.',
                'price': 85.00,
                'category': 'Casual',
                'brand': 'Adidas',
                'gender': 'U',
                'featured': False,
            },
        ]
        
        # Create products
        for product_data in products_data:
            category = Category.objects.get(name=product_data.pop('category'))
            brand = Brand.objects.get(name=product_data.pop('brand'))
            
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    **product_data,
                    'category': category,
                    'brand': brand,
                    'in_stock': True
                }
            )
            
            # Add sizes
            if created:
                sizes = [7.0, 8.0, 9.0, 10.0, 11.0, 12.0]
                for size in sizes:
                    ProductSize.objects.create(
                        product=product,
                        size=size,
                        quantity=10
                    )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )