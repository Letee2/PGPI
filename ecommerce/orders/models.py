from django.db import models
from shop.models import Product
from django.contrib.auth.models import User

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('standard', 'Entrega Estándar (5.00€)'),
        ('express', 'Entrega Express (10.00€)'),
        ('free', 'Envío Gratuito'),
    ]
    
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES, default='standard')
    delivery_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all()) + self.delivery_cost


    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    email = models.EmailField()
    address = models.TextField()
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    tracking_id = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Pedido {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def get_cost(self):
        return self.price * self.quantity
