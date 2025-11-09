from shoestore.models import Cart

def cart_items_count(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        cart = Cart.objects.filter(session_key=session_key).first() if session_key else None
    
    cart_count = cart.items.count() if cart else 0
    return {'cart_items_count': cart_count}