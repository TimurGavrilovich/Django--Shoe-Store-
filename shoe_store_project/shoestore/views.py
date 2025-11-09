from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from shoestore.models import Product, Category, Brand, Cart, CartItem
import json

def home(request):
    featured_products = Product.objects.filter(featured=True, in_stock=True)[:12]  # Increased from 8 to 12
    new_arrivals = Product.objects.filter(in_stock=True).order_by('-created_at')[:12]  # Increased from 8 to 12
    
    context = {
        'featured_products': featured_products,
        'new_arrivals': new_arrivals,
    }
    return render(request, 'home.html', context)

def product_list(request):
    products = Product.objects.filter(in_stock=True)
    categories = Category.objects.all()
    brands = Brand.objects.all()
    
    # Filtering
    category_slug = request.GET.get('category')
    brand_slug = request.GET.get('brand')
    gender = request.GET.get('gender')
    search = request.GET.get('search')
    
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if brand_slug:
        products = products.filter(brand__name=brand_slug)
    if gender:
        products = products.filter(gender=gender)
    if search:
        products = products.filter(
            Q(name__icontains=search) | 
            Q(description__icontains=search) |
            Q(brand__name__icontains=search)
        )
    
    # Sorting
    sort = request.GET.get('sort', 'name')
    if sort == 'price_low':
        products = products.order_by('price')
    elif sort == 'price_high':
        products = products.order_by('-price')
    elif sort == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('name')
    
    context = {
        'products': products,
        'categories': categories,
        'brands': brands,
    }
    return render(request, 'product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id).filter(in_stock=True)[:4]
    
    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'product_detail.html', context)

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

def add_to_cart(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        product_id = data.get('product_id')
        size = data.get('size')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id)
        cart = get_or_create_cart(request)
        
        # Check if item already exists in cart
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            size=size,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        return JsonResponse({'success': True, 'cart_count': cart.items.count()})
    
    return JsonResponse({'success': False})

def cart_view(request):
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context)

def update_cart_item(request, item_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        quantity = data.get('quantity')
        
        cart_item = get_object_or_404(CartItem, id=item_id, cart=get_or_create_cart(request))
        
        if quantity == 0:
            cart_item.delete()
        else:
            cart_item.quantity = quantity
            cart_item.save()
        
        cart = get_or_create_cart(request)
        return JsonResponse({
            'success': True,
            'item_total': cart_item.total_price,
            'cart_total': cart.total_price,
            'cart_count': cart.items.count()
        })
    
    return JsonResponse({'success': False})

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart=get_or_create_cart(request))
        cart_item.delete()
        
        cart = get_or_create_cart(request)
        return JsonResponse({
            'success': True,
            'cart_total': cart.total_price,
            'cart_count': cart.items.count()
        })
    
    return JsonResponse({'success': False})