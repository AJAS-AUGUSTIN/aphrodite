from .models import Cart, CartItems, WishCart, Wishlist
from .views import _cart_id,_wishcart_id


def wish_list(request):
    if request.user.is_authenticated:
        wish_items_count = Wishlist.objects.filter(user = request.user).count()
    else:
        wish_items_count = 0
    return{'wish_items': wish_items_count}

def counter(request):
        if request.user.is_authenticated:
            cart_items_count = CartItems.objects.filter(user = request.user).count()
            return{'cart_count': cart_items_count}
        else:
            if request.session.has_key('guest_cart'):
                cart = request.session['guest_cart']
                cart_items_count = CartItems.objects.filter(cart = cart).count()
            else:
                cart_items_count = 0
            return{'cart_count': cart_items_count}

