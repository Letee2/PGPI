from django.test import TestCase
from django.urls import reverse
from shop.models import Category, Product

class ShopTests(TestCase):

    def setUp(self):
        # Crear categorías
        self.category1 = Category.objects.create(name="Lavadoras", slug="lavadoras")
        self.category2 = Category.objects.create(name="Refrigeradores", slug="refrigeradores")
        
        # Crear productos
        self.product1 = Product.objects.create(
            category=self.category1,
            name="Lavadora LG TurboWash",
            slug="lavadora-lg-turbowash",
            description="Lavadora de alta eficiencia.",
            price=499.99,
            stock=10,
            available=True,
        )
        self.product2 = Product.objects.create(
            category=self.category2,
            name="Refrigerador Samsung 400L",
            slug="refrigerador-samsung-400l",
            description="Refrigerador con tecnología avanzada.",
            price=699.99,
            stock=5,
            available=True,
        )
        self.product3 = Product.objects.create(
            category=self.category2,
            name="Refrigerador LG 300L",
            slug="refrigerador-lg-300l",
            description="Refrigerador con sistema eficiente.",
            price=599.99,
            stock=0,  # Producto agotado
            available=True,
        )

    def test_product_list_view(self):
        # Testear acceso a la lista de productos
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/list.html')
        self.assertContains(response, "Lavadora LG TurboWash")
        self.assertContains(response, "Refrigerador Samsung 400L")

    def test_product_list_by_category_view(self):
        # Testear acceso a los productos por categoría
        response = self.client.get(reverse('shop:product_list_by_category', args=[self.category2.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Refrigerador Samsung 400L")
        self.assertContains(response, "Refrigerador LG 300L")
        self.assertNotContains(response, "Lavadora LG TurboWash")

    def test_product_detail_view(self):
        # Testear acceso a la vista de detalle de un producto
        response = self.client.get(reverse('shop:product_detail', args=[self.product1.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/product/detail.html')
        self.assertContains(response, "Lavadora LG TurboWash")
        self.assertContains(response, "Lavadora de alta eficiencia.")

    def test_out_of_stock_product(self):
        # Testear que un producto agotado aparece correctamente
        response = self.client.get(reverse('shop:product_list_by_category', args=[self.category2.slug]))
        self.assertContains(response, "Refrigerador LG 300L")
        self.assertContains(response, "Agotado")

    def test_invalid_category(self):
        # Testear acceso a una categoría inexistente
        response = self.client.get(reverse('shop:product_list_by_category', args=["no-existe"]))
        self.assertEqual(response.status_code, 404)
