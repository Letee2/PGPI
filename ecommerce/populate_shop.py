import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from shop.models import Category, Product

def populate_shop():
    # Crear categorías
    categories = [
        {"name": "Lavadoras", "slug": "lavadoras"},
        {"name": "Refrigeradores", "slug": "refrigeradores"},
        {"name": "Microondas", "slug": "microondas"},
        {"name": "Pequeños Electrodomésticos", "slug": "pequenos-electrodomesticos"},
    ]
    
    category_objects = []
    for category in categories:
        obj, created = Category.objects.get_or_create(**category)
        category_objects.append(obj)

    # Crear productos con fabricante y algunos sin stock
    products = [
        {
            "name": "Lavadora LG TurboWash",
            "slug": "lavadora-lg-turbowash",
            "description": "Lavadora de alta eficiencia con tecnología TurboWash.",
            "price": 499.99,
            "stock": 10,
            "available": True,
            "manufacturer": "LG",
            "category": category_objects[0],
        },
        {
            "name": "Refrigerador Samsung 400L",
            "slug": "refrigerador-samsung-400l",
            "description": "Refrigerador con tecnología de enfriamiento avanzado.",
            "price": 699.99,
            "stock": 0,  # Producto sin stock
            "available": False,
            "manufacturer": "Samsung",
            "category": category_objects[1],
        },
        {
            "name": "Microondas Panasonic Compacto",
            "slug": "microondas-panasonic-compacto",
            "description": "Microondas de tamaño compacto con múltiples funciones.",
            "price": 199.99,
            "stock": 20,
            "available": True,
            "manufacturer": "Panasonic",
            "category": category_objects[2],
        },
        {
            "name": "Cafetera Nespresso Inissia",
            "slug": "cafetera-nespresso-inissia",
            "description": "Cafetera compacta y fácil de usar.",
            "price": 89.99,
            "stock": 15,
            "available": True,
            "manufacturer": "Nespresso",
            "category": category_objects[3],
        },
        {
            "name": "Hervidor de Agua Philips",
            "slug": "hervidor-agua-philips",
            "description": "Hervidor de agua eléctrico con diseño moderno.",
            "price": 49.99,
            "stock": 0,  # Producto sin stock
            "available": False,
            "manufacturer": "Philips",
            "category": category_objects[3],
        },
    ]

    for product in products:
        # Verificar si el producto ya existe
        obj, created = Product.objects.get_or_create(slug=product["slug"], defaults=product)
        if created:
            print(f"Producto creado: {obj.name}")
        else:
            print(f"Producto ya existente: {obj.name}")

    print("¡Base de datos poblada con éxito!")

if __name__ == "__main__":
    populate_shop()
