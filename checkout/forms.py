from django import forms
from .models import Order


class MakePaymentForm(forms.Form):
    MONTH_CHOICES = [(i, i) for i in range(1, 13)]
    YEAR_CHOICES = [(i, i) for i in range(2019, 2036)]
    
    # Stripe Javascript deals with data in form, encryption etc. therefore 
    # we can put required=False so plain text is not transmitted through the browser
    credit_card_number = forms.CharField(label='Credit card number', required=False)
    cvv = forms.CharField(label='Security code (CVV)', required=False)
    expiry_month = forms.ChoiceField(label='Month', 
                                     choices=MONTH_CHOICES, 
                                     required=False)
    expiry_year = forms.ChoiceField(label='Year', 
                                    choices=YEAR_CHOICES, 
                                    required=False)
    # Stripe requires an id. This field inputs a value that is not shown
    stripe_id = forms.CharField(widget=forms.HiddenInput)
        
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'phone_number', 'country', 'postcode', 'town_or_city',
                  'street_address1', 'street_address2', 'county')

