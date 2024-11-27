from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    payment_method = models.CharField(
        max_length=20,
        choices=[('stripe', 'Stripe'), ('cash', 'Contra Reembolso')],
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.user.email
    
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = None  # Eliminar el campo de nombre de usuario
    email = models.EmailField(unique=True)  # Hacer que el correo sea único y requerido

    USERNAME_FIELD = 'email'  # Definir el correo como identificador principal
    REQUIRED_FIELDS = []  # No se requieren otros campos adicionales

    def __str__(self):
        return self.email


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()