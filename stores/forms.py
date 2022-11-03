from django import forms

from . models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ['cart','amount','order_status','discount','subtotal','payment_completed','ref']
        widgets = {
            'ordered_by': forms.TextInput(attrs={'class':'form-control'}),
            'shipping_address': forms.TextInput(attrs={'class':'form-control'}),
            'phone': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.TextInput(attrs={'class':'form-control'}),
            'payment_method': forms.TextInput(attrs={'class':'form-control'}),
        }