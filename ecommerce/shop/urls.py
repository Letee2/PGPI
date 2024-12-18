from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('catalogo/', views.product_list, name='product_list'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
