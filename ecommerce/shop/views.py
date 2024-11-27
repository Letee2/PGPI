from django.shortcuts import render, get_object_or_404
from .models import Category, Product

from django.db.models import Q

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.all()

    # Buscar por nombre, categoría o fabricante
    query = request.GET.get('query')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(category__name__icontains=query) | Q(manufacturer__icontains=query)
        )

    # Filtrar por categoría
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


from django.http import HttpResponseRedirect
from django.urls import reverse
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)

    # Redirigir si el producto está agotado
    if product.stock <= 0 or not product.available:
        return HttpResponseRedirect(reverse('shop:product_list'))

    return render(request, 'shop/product/detail.html', {'product': product})