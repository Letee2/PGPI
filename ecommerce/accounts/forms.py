from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,CustomUser

class CustomUserCreationForm(UserCreationForm):
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="La contraseña debe contener al menos 8 caracteres y no ser completamente numérica.",
    )
    password2 = forms.CharField(
        label="Confirmar Contraseña",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        help_text="Introduce la misma contraseña para verificarla.",
    )

    class Meta:
        model = CustomUser
        fields = ['email']
        labels = {
            'email': 'Correo Electrónico',
        }
        widgets = {
            'email': forms.EmailInput(attrs={"class": "form-control"}),
        }

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