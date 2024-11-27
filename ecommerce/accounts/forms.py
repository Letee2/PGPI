from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    email = forms.EmailField(
        disabled=True,
        required=False,
        initial=lambda: None,
        label="Correo Electrónico (No editable)"
    )

    class Meta:
        model = Profile
        fields = ['address', 'postal_code', 'city', 'payment_method']
        labels = {
            'address': 'Dirección',
            'postal_code': 'Código Postal',
            'city': 'Ciudad',
            'payment_method': 'Método de Pago',
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['email'].initial = user.email