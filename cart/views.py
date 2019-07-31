from django.shortcuts import render, redirect, reverse



def view_cart(request):
    """Render all cart contents"""
    # no need to pass dict with contents as they are available as context
    # everywhere
    return render(request, 'cart.html') 


def add_to_cart(request, id):
    """Add a quantity of the specified product in the cart"""
    # To increase/decrease number of items in cart, throught a button in form
    quantity = int(request.POST.get('quantity'))
    
    # It gets the cart from the session, not from a database etc.
    # It gets a dict with the items on the cart, or an empty dict if none
    cart = request.session.get('cart', {})
    
    if id in cart:
        cart[id] = int(cart[id]) + quantity      
    else:
        cart[id] = cart.get(id, quantity) 

    request.session['cart'] = cart
    return redirect(reverse('index'))


def adjust_cart(request, id):
    """Adjust the quantity of the specified product to the specified amount"""
    quantity = int(request.POST.get('quantity'))
    cart = request.session.get('cart', {})
    # only adjust if there is something in the cart
    if quantity > 0:
        cart[id] = quantity
    else:
        cart.pop(id)
    request.session['cart'] = cart
    return redirect(reverse('view_cart'))
