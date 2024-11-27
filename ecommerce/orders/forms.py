from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    delivery_method = forms.ChoiceField(
        choices=Order.DELIVERY_CHOICES,
        widget=forms.RadioSelect,
        label="Método de entrega"
    )

    class Meta:
        model = Order
        fields = ['email', 'address', 'postal_code', 'city', 'delivery_method']
        labels = {
            'address': 'Dirección',
            'postal_code': 'Código Postal',
            'city': 'Ciudad',
            'payment_method': 'Método de Pago',
        }

class PaymentMethodForm(forms.Form):
    PAYMENT_CHOICES = [
        ('cod', 'Contra Reembolso'),
        ('stripe', 'Tarjeta de Crédito (Stripe)'),
    ]
    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES, widget=forms.RadioSelect,label='Elija un método de pago')
    
