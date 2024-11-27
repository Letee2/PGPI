from django.test import TestCase
from django.urls import reverse
from shop.models import Category, Product
from orders.models import Order, OrderItem

class OrderTests(TestCase):
    def setUp(self):
        # Crear productos de prueba
        self.category = Category.objects.create(name="Electrodomésticos", slug="electrodomesticos")
        self.product1 = Product.objects.create(
            category=self.category,
            name="Lavadora",
            slug="lavadora",
            price=500.00,
            stock=10,
            available=True,
        )
        self.product2 = Product.objects.create(
            category=self.category,
            name="Refrigerador",
            slug="refrigerador",
            price=800.00,
            stock=5,
            available=True,
        )

        # Crear sesión de carrito simulada
        self.client.session['cart'] = {
            str(self.product1.id): {'quantity': 2, 'price': str(self.product1.price)},
            str(self.product2.id): {'quantity': 1, 'price': str(self.product2.price)},
        }
        self.client.session.save()

    def test_order_creation(self):
        # Simular creación de pedido
        response = self.client.post(reverse('orders:order_create'), {
            'email': 'test@example.com',
            'address': '123 Test St',
            'postal_code': '12345',
            'city': 'Testville',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 2)

        order = Order.objects.first()
        self.assertEqual(order.email, 'test@example.com')
        self.assertEqual(order.get_total_cost(), 1800.00)

    def test_order_tracking(self):
        # Crear un pedido y probar el seguimiento
        order = Order.objects.create(
            email='test@example.com',
            address='123 Test St',
            postal_code='12345',
            city='Testville',
            tracking_id='test-tracking-id',
        )
        response = self.client.get(reverse('orders:order_track', args=[order.tracking_id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'test-tracking-id')
        self.assertContains(response, '123 Test St')
