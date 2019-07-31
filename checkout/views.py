from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.utils import timezone
from products.models import Product
import stripe


stripe.api_key = settings.STRIPE_SECRET


@login_required
def checkout(request):
    if request.method == 'POST':
        # get customer info
        order_form = OrderForm(request.POST)
        # card details
        payment_form = MakePaymentForm(request.POST)
        print('\n\norder_form\n', order_form.is_valid(), order_form)
        print('\n\npayment_form\n', payment_form.is_valid(), payment_form)
        if order_form.is_valid() and payment_form.is_valid():
            # commit=False is to save data and keep form open to add 
            # more data before saving
            order = order_form.save(commit=False)
            order.date = timezone.now()
            order.save()
            
            cart = request.session.get('cart', {})
            total = 0
            
            for id, quantity in cart.items():
                product = get_object_or_404(Product, pk=id)
                total += quantity * product.price
                order_line_item = OrderLineItem(
                    order = order,
                    product = product,
                    quantity = quantity
                    )
                order_line_item.save()
            try:
                # In stripe €10.00 is 1000
                customer = stripe.Charge.create(
                    amount = int(total * 100),
                    currency = 'EUR',
                    description = request.user.email,
                    card = payment_form.cleaned_data['stripe_id'],
                    )
            except stripe.error.CardError:
                messages.error(request, 'Your card was declined')
            
            if customer.paid:
                messages.error(request, 'You have successfully paid')
                request.session['cart'] = {}
                return redirect(reverse('products'))
            else:
                messages.error(request, 'Unable to take payment')
        else:
            print(payment_form.errors)
            messages.error(request, 'We were unable to take payment with that card!')
    else:
        # if the request is not POST request, just return blank forms
        payment_form = MakePaymentForm()
        order_form = OrderForm()
    
    return render(request, 
                  'checkout.html', 
                  {'order_form': order_form,
                  'payment_form': payment_form,
                  'publishable': settings.STRIPE_PUBLISHABLE},
                 )
