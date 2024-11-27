from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'postal_code', 'city', 'payment_method')  # Columnas visibles en la lista
    list_filter = ('city', 'payment_method')  # Filtros laterales
    search_fields = ('user__username', 'user__email', 'address')  # Campos para buscar
