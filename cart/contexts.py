from django.shortcuts import get_object_or_404
from products.models import Product


def cart_content(request):
    """
    Makes cart contents available on any page
    """
    cart =  request.session.get('cart', {})
    cart_items = []
    total = 0
    product_count = 0
    
    for id, quantity in cart.items():
        product = get_object_or_404(Product, pk=id)
        product_count += quantity
        total += quantity * product.price
        cart_items.append({'id': id, 'quantity': quantity, 'product': product})
        
    return {'cart_items': cart_items, 
            'total': total, 
            'product_count': product_count}
        