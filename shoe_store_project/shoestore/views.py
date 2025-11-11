from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Product, Category, Brand, Cart, CartItem
import json

def home(request):
    featured_products = Product.objects.filter(featured=True, in_stock=True)[:12]
    new_arrivals = Product.objects.filter(in_stock=True).order_by('-created_at')[:12]
    
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
    
    # сортировка 
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
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            size = data.get('size')
            quantity = int(data.get('quantity', 1))
            
            if not size:
                return JsonResponse({'success': False, 'error': 'Please select a size'})
            
            product = get_object_or_404(Product, id=product_id)
            cart = get_or_create_cart(request)
            
            # Проверка есть  если в корзине есть товар 
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
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def cart_view(request):
    cart = get_or_create_cart(request)
    
    # Если пользователь авторизировался , совмещаем корзины
    if request.user.is_authenticated and not request.session.get('cart_merged'):
        merge_guest_cart_with_user(request)
        request.session['cart_merged'] = True
    
    context = {
        'cart': cart,
    }
    return render(request, 'cart.html', context)

def update_cart_item(request, item_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            quantity = data.get('quantity')
            
            cart = get_or_create_cart(request)
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            
            if quantity == 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()
            
            cart = get_or_create_cart(request)
            return JsonResponse({
                'success': True,
                'item_total': cart_item.total_price if quantity > 0 else 0,
                'cart_total': cart.total_price,
                'cart_count': cart.items.count()
            })
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        try:
            cart = get_or_create_cart(request)
            cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
            cart_item.delete()
            
            cart = get_or_create_cart(request)
            return JsonResponse({
                'success': True,
                'cart_total': cart.total_price,
                'cart_count': cart.items.count()
            })
        
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

def merge_guest_cart_with_user(request):
    """Merge guest cart items into user cart after login"""
    if request.user.is_authenticated:
        session_key = request.session.session_key
        if session_key:
            # достаем корзину пользователя
            guest_cart = Cart.objects.filter(session_key=session_key).first()
            # достаем или создаем корзину пользователя
            user_cart, created = Cart.objects.get_or_create(user=request.user)
            
            if guest_cart and guest_cart != user_cart:
                # совмещаем товар с двух карзин
                for guest_item in guest_cart.items.all():
                    user_item, item_created = CartItem.objects.get_or_create(
                        cart=user_cart,
                        product=guest_item.product,
                        size=guest_item.size,
                        defaults={'quantity': guest_item.quantity}
                    )
                    
                    if not item_created:
                        # если товар уже в корзине , добавляем его кол-во
                        user_item.quantity += guest_item.quantity
                        user_item.save()
                
                # удаляем карзину
                guest_cart.delete()
                
                return True
    
    return False

# аутентификация
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # авто логин после регистрации 
            login(request, user)
            messages.success(request, f'Welcome to StepStyle, {user.username}! Your account has been created successfully.')
            
            # добавляем товар из корзины 
            merge_guest_cart_with_user(request)
            request.session['cart_merged'] = True
            
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                
                # совмещаем корзины 
                merge_guest_cart_with_user(request)
                request.session['cart_merged'] = True
                
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

@login_required
def profile_view(request):
    user_carts = Cart.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'registration/profile.html', {'user_carts': user_carts})