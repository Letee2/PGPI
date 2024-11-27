from django.test import TestCase
from django.urls import reverse
from .models import Category, Product

class ShopViewsTests(TestCase):

    def setUp(self):
        # Crear una categoría
        self.category = Category.objects.create(name="Category 1", slug="category-1")

        # Crear productos
        self.product_in_stock = Product.objects.create(
            name="Product In Stock",
            slug="product-in-stock",
            category=self.category,
            price=10.00,
            stock=10,
            available=True
        )
        self.product_out_of_stock = Product.objects.create(
            name="Product Out of Stock",
            slug="product-out-of-stock",
            category=self.category,
            price=20.00,
            stock=0,
            available=True
        )

    def test_product_list_view(self):
        response = self.client.get(reverse('shop:product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product_in_stock, response.context['products'])
        self.assertIn(self.product_out_of_stock, response.context['products'])  # Asegurarnos que aparece

    def test_product_list_view_with_category(self):
        response = self.client.get(reverse('shop:product_list_by_category', args=[self.category.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product_in_stock, response.context['products'])
        self.assertIn(self.product_out_of_stock, response.context['products'])  # Los productos agotados también aparecen

    def test_product_detail_view_in_stock(self):
        response = self.client.get(reverse('shop:product_detail', args=[self.product_in_stock.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product_in_stock.name)
        self.assertContains(response, "En stock")

    def test_landing_page_view(self):
        response = self.client.get(reverse('shop:landing_page'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product_in_stock, response.context['featured_products'])
        self.assertIn(self.product_out_of_stock, response.context['featured_products'])  # Los productos agotados deben estar presentes
