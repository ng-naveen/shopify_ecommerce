from store.models import Cart


def cart_item_count(request):
    if request.user.is_authenticated:
        cart_quantity = Cart.objects.filter(user=request.user, status='in-cart').count()
    else:
        cart_quantity = 0
    return {'cart_quantity':cart_quantity}

