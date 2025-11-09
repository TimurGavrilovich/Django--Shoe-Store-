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
        
        # Sample products data with real shoe images from Unsplash
        products_data = [
            {
                'name': 'Nike Air Max 270',
                'slug': 'nike-air-max-270',
                'description': 'The Nike Air Max 270 delivers comfortable style and incredible energy return with the largest Air unit yet.',
                'price': 150.00,
                'discount_price': 129.99,
                'category': 'Sneakers',
                'brand': 'Nike',
                'gender': 'U',
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8bmlrZSUyMHNob2VzfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Adidas Ultraboost 21',
                'slug': 'adidas-ultraboost-21',
                'description': 'Experience incredible energy return and comfort with Adidas Ultraboost running shoes.',
                'price': 180.00,
                'category': 'Running',
                'brand': 'Adidas',
                'gender': 'U',
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8YWRpZGFzJTIwc2hvZXN8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Puma RS-X',
                'slug': 'puma-rs-x',
                'description': 'Bold designs and comfortable fit with Puma RS-X sneakers. Perfect for urban lifestyle.',
                'price': 110.00,
                'category': 'Sneakers',
                'brand': 'Puma',
                'gender': 'U',
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1605348532760-6753d2c43329?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fHB1bWElMjBzaG9lc3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'New Balance 574',
                'slug': 'new-balance-574',
                'description': 'Classic style meets modern comfort with New Balance 574. Timeless design for everyday wear.',
                'price': 89.99,
                'category': 'Casual',
                'brand': 'New Balance',
                'gender': 'U',
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1549289524-06cf8837ace5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8bmV3JTIwYmFsYW5jZSUyMHNob2VzfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Vans Old Skool',
                'slug': 'vans-old-skool',
                'description': 'The iconic Vans Old Skool with timeless style and durability. Perfect for skateboarding and casual wear.',
                'price': 65.00,
                'category': 'Casual',
                'brand': 'Vans',
                'gender': 'U',
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8dmFucyUyMHNob2VzfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Converse Chuck Taylor',
                'slug': 'converse-chuck-taylor',
                'description': 'The classic Converse Chuck Taylor All Star sneakers. A timeless design that never goes out of style.',
                'price': 55.00,
                'discount_price': 45.00,
                'category': 'Casual',
                'brand': 'Converse',
                'gender': 'U',
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8Y29udmVyc2UlMjBzaG9lc3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Nike Air Force 1',
                'slug': 'nike-air-force-1',
                'description': 'The classic Nike Air Force 1 in white with premium leather. A basketball icon turned streetwear staple.',
                'price': 100.00,
                'category': 'Sneakers',
                'brand': 'Nike',
                'gender': 'U',
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1595950653106-6c9ebd614d3a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8bmlrZSUyMGFpciUyMGZvcmNlJTIwMXxlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Adidas Stan Smith',
                'slug': 'adidas-stan-smith',
                'description': 'Clean, minimalist design with the iconic Adidas Stan Smith. The perfect white sneaker for any occasion.',
                'price': 85.00,
                'category': 'Casual',
                'brand': 'Adidas',
                'gender': 'U',
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1587563871167-1ee9c731aefb?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NXx8YWRpZGFzJTIwc3RhbiUyMHNtaXRofGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Nike Dunk Low',
                'slug': 'nike-dunk-low',
                'description': 'The Nike Dunk Low returns with classic colors and timeless basketball style.',
                'price': 110.00,
                'discount_price': 95.00,
                'category': 'Sneakers',
                'brand': 'Nike',
                'gender': 'U',
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1600269452121-4f2416e55c28?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8bmlrZSUyMGR1bmt8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Running Trail Shoes',
                'slug': 'running-trail-shoes',
                'description': 'Professional trail running shoes with superior grip and cushioning for rough terrains.',
                'price': 140.00,
                'category': 'Running',
                'brand': 'New Balance',
                'gender': 'U',
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1460353581641-37baddab0fa2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8cnVubmluZyUyMHNob2VzfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Leather Formal Shoes',
                'slug': 'leather-formal-shoes',
                'description': 'Elegant leather formal shoes perfect for business meetings and special occasions.',
                'price': 120.00,
                'category': 'Formal',
                'brand': 'Puma',
                'gender': 'M',
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1529810313688-44ea1c2d131d?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8Zm9ybWFsJTIwc2hvZXN8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Winter Boots',
                'slug': 'winter-boots',
                'description': 'Warm and durable winter boots designed to keep your feet comfortable in cold weather.',
                'price': 95.00,
                'category': 'Boots',
                'brand': 'Vans',
                'gender': 'U',
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Ym9vdHN8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Basketball Shoes',
                'slug': 'basketball-shoes',
                'description': 'High-performance basketball shoes with excellent ankle support and traction.',
                'price': 130.00,
                'category': 'Sneakers',
                'brand': 'Nike',
                'gender': 'M',
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1608231387042-66d1773070a5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8M3x8YmFza2V0YmFsbCUyMHNob2VzfGVufDB8fDB8fHww&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Women Running Shoes',
                'slug': 'women-running-shoes',
                'description': 'Lightweight running shoes designed specifically for women with enhanced comfort features.',
                'price': 115.00,
                'category': 'Running',
                'brand': 'Adidas',
                'gender': 'W',
                'featured': False,
                'image_url': 'https://images.unsplash.com/photo-1551107696-a4b0c5a0d9a2?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTF8fHJ1bm5pbmclMjBzaG9lc3xlbnwwfHwwfHx8MA%3D%3D&auto=format&fit=crop&w=500&q=60'
            },
            {
                'name': 'Fashion Sneakers',
                'slug': 'fashion-sneakers',
                'description': 'Trendy fashion sneakers that combine style and comfort for everyday wear.',
                'price': 75.00,
                'discount_price': 65.00,
                'category': 'Sneakers',
                'brand': 'Converse',
                'gender': 'W',
                'featured': True,
                'image_url': 'https://images.unsplash.com/photo-1575537302964-96cd47c06b1b?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OXx8c25lYWtlcnN8ZW58MHx8MHx8fDA%3D&auto=format&fit=crop&w=500&q=60'
            }
        ]
        
        # Create products
        for product_data in products_data:
            category = Category.objects.get(name=product_data.pop('category'))
            brand = Brand.objects.get(name=product_data.pop('brand'))
            image_url = product_data.pop('image_url')
            
            product, created = Product.objects.get_or_create(
                slug=product_data['slug'],
                defaults={
                    **product_data,
                    'category': category,
                    'brand': brand,
                    'in_stock': True,
                    'image_url': image_url
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
            self.style.SUCCESS('Successfully populated database with sample data and real shoe images!')
        )