from django.test import TestCase
from django.urls import reverse
from shop.models import Category, Product

class CartTests(TestCase):
    def setUp(self):
        # Crear categorías y productos de prueba
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

    def test_add_product_to_cart(self):
        # Agregar un producto al carrito
        response = self.client.post(reverse('cart:cart_add', args=[self.product1.id]), {'quantity': 1})
        self.assertEqual(response.status_code, 302)  # Redirección al detalle del carrito
        session = self.client.session
        self.assertIn(str(self.product1.id), session['cart'])
        self.assertEqual(session['cart'][str(self.product1.id)]['quantity'], 1)

    def test_update_product_quantity_in_cart(self):
        # Agregar un producto y luego actualizar la cantidad
        self.client.post(reverse('cart:cart_add', args=[self.product1.id]), {'quantity': 1})
        self.client.post(reverse('cart:cart_add', args=[self.product1.id]), {'quantity': 2, 'override': True})
        session = self.client.session
        self.assertEqual(session['cart'][str(self.product1.id)]['quantity'], 2)

    def test_remove_product_from_cart(self):
        # Agregar y luego eliminar un producto del carrito
        self.client.post(reverse('cart:cart_add', args=[self.product1.id]), {'quantity': 1})
        self.client.post(reverse('cart:cart_remove', args=[self.product1.id]))
        session = self.client.session
        self.assertNotIn(str(self.product1.id), session['cart'])

    def test_cart_total_price(self):
        # Validar el precio total del carrito
        self.client.post(reverse('cart:cart_add', args=[self.product1.id]), {'quantity': 2})
        self.client.post(reverse('cart:cart_add', args=[self.product2.id]), {'quantity': 1})
        session = self.client.session
        total_price = sum(
            float(item['price']) * item['quantity'] for item in session['cart'].values()
        )
        self.assertEqual(total_price, 1800.00)
