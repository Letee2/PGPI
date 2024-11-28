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
        {"name": "Aspiradoras", "slug": "aspiradoras"},
    ]
    
    category_objects = []
    for category in categories:
        obj, created = Category.objects.get_or_create(**category)
        category_objects.append(obj)

    # Crear productos con fabricante y algunos sin stock
    products = [
        # Lavadoras
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
            "name": "Lavadora Samsung EcoBubble",
            "slug": "lavadora-samsung-ecobubble",
            "description": "Lavadora silenciosa y ecológica con capacidad de 9kg.",
            "price": 599.99,
            "stock": 5,
            "available": True,
            "manufacturer": "Samsung",
            "category": category_objects[0],
        },
        # Refrigeradores
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
            "name": "Refrigerador LG InstaView",
            "slug": "refrigerador-lg-instaview",
            "description": "Refrigerador con puerta de vidrio y dispensador de agua.",
            "price": 1099.99,
            "stock": 3,
            "available": True,
            "manufacturer": "LG",
            "category": category_objects[1],
        },
        # Microondas
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
            "name": "Microondas Whirlpool Digital",
            "slug": "microondas-whirlpool-digital",
            "description": "Microondas con pantalla digital y 10 programas automáticos.",
            "price": 249.99,
            "stock": 10,
            "available": True,
            "manufacturer": "Whirlpool",
            "category": category_objects[2],
        },
        # Pequeños Electrodomésticos
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
            "name": "Batidora Philips Viva",
            "slug": "batidora-philips-viva",
            "description": "Batidora de mano potente con múltiples accesorios.",
            "price": 59.99,
            "stock": 12,
            "available": True,
            "manufacturer": "Philips",
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
        # Aspiradoras
        {
            "name": "Aspiradora Dyson V11",
            "slug": "aspiradora-dyson-v11",
            "description": "Aspiradora inalámbrica con gran potencia de succión.",
            "price": 599.99,
            "stock": 7,
            "available": True,
            "manufacturer": "Dyson",
            "category": category_objects[4],
        },
        {
            "name": "Aspiradora Rowenta Compact Power",
            "slug": "aspiradora-rowenta-compact-power",
            "description": "Aspiradora con bolsa para una limpieza eficiente.",
            "price": 149.99,
            "stock": 10,
            "available": True,
            "manufacturer": "Rowenta",
            "category": category_objects[4],
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
