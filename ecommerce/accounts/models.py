from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings

# Custom User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo electrónico debe proporcionarse")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("El superusuario debe tener is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("El superusuario debe tener is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

# Custom User Model
class CustomUser(AbstractUser):
    username = None  # Eliminar el campo de nombre de usuario
    email = models.EmailField(unique=True)  # Hacer que el correo sea único y requerido

    USERNAME_FIELD = 'email'  # Definir el correo como identificador principal
    REQUIRED_FIELDS = []  # No se requieren otros campos adicionales

    objects = CustomUserManager()  # Usar el manager personalizado

    def __str__(self):
        return self.email

# Profile Model
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