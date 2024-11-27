from django.contrib import admin
from .models import Order, OrderItem
from django.utils.html import format_html
from django.urls import reverse
import csv
from django.http import HttpResponse

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.action(description="Exportar Pedidos a CSV")
def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="pedidos.csv"'
    writer = csv.writer(response)
    writer.writerow(['ID', 'Usuario', 'Correo', 'Dirección', 'Código Postal', 'Ciudad', 'Total', 'Pagado', 'Creado'])
    for order in queryset:
        writer.writerow([
            order.id, 
            order.user.username if order.user else "No registrado", 
            order.email, 
            order.address, 
            order.postal_code, 
            order.city, 
            order.get_total_cost(), 
            "Sí" if order.paid else "No", 
            order.created,
        ])
    return response

@admin.action(description='Marcar como pagado')
def mark_as_paid(modeladmin, request, queryset):
    queryset.update(paid=True)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'email', 'city', 'paid', 'created', 'updated', 'total_cost')
    list_filter = ('paid', 'created', 'updated', 'delivery_method')
    search_fields = ('email', 'tracking_id', 'user__username')
    actions = [mark_as_paid, export_to_csv]
    inlines = [OrderItemInline]
    readonly_fields = ('created', 'updated', 'tracking_id')

    def total_cost(self, obj):
        return f"{obj.get_total_cost()} €"
    total_cost.short_description = 'Costo Total'

