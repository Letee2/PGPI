from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
        return self.user.username
