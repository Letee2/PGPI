from django.shortcuts import render, redirect
from django.core.mail import send_mail
from cart.models import Cart
from .models import Order, OrderItem
from .forms import OrderCreateForm,PaymentMethodForm
import uuid
from django.urls import reverse 
from django.conf import settings
import stripe
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.conf import settings

def order_create(request):
    cart = Cart(request)

    # Redirigir a completar perfil si faltan datos del usuario autenticado
    if request.user.is_authenticated:
        profile = request.user.profile
        if not profile.address or not profile.postal_code or not profile.city:
            messages.warning(request, "Por favor completa tu perfil antes de realizar un pedido.")
            return redirect('accounts:profile')

    if request.method == 'POST':
        return handle_post_request(request, cart)
    else:
        return handle_get_request(request, cart)


def handle_post_request(request, cart):
    form = OrderCreateForm(request.POST)
    payment_form = PaymentMethodForm(request.POST)
    if form.is_valid() and payment_form.is_valid():
        order = create_order(request, form,cart)
        create_order_items(order, cart)
        cart.clear()

        payment_method = payment_form.cleaned_data['payment_method']
        if payment_method == 'stripe':
            return process_stripe_payment(request, order)
        else:
            return process_cash_on_delivery(order)

    return render(request, 'orders/order/create.html', {
        'cart': cart,
        'form': form,
        'payment_form': payment_form,
    })


def handle_get_request(request, cart):
    delivery_choices = [
        ('standard', 'Entrega Estándar (5.00€)'),
        ('express', 'Entrega Express (10.00€)'),
    ]

    # Modificar las opciones de entrega según el importe total del carrito
    if cart.get_total_price() >= 100:
        # Si el total es mayor o igual a 100€, solo mostrar "Envío Gratuito" y "Entrega Express"
        delivery_choices = [
            ('free', 'Envío Gratuito'),
            ('express', 'Entrega Express (10.00€)'),
        ]

    # Crear el formulario de pedido con datos iniciales
    if request.user.is_authenticated:
        profile = request.user.profile
        initial_data = {
            'email': request.user.email,
            'address': profile.address,
            'postal_code': profile.postal_code,
            'city': profile.city,
        }
        form = OrderCreateForm(initial=initial_data)
    else:
        form = OrderCreateForm()

    # Asignar las opciones de entrega al campo correspondiente
    form.fields['delivery_method'].choices = delivery_choices

    # Crear el formulario de método de pago
    payment_form = PaymentMethodForm()

    # Renderizar la plantilla con los formularios y el carrito
    return render(request, 'orders/order/create.html', {
        'cart': cart,
        'form': form,
        'payment_form': payment_form,
    })

def create_order(request, form, cart):
    order = form.save(commit=False)
    if request.user.is_authenticated:
        order.user = request.user
    order.tracking_id = str(uuid.uuid4())

    # Calcular costo de envío
    if form.cleaned_data['delivery_method'] == 'standard':
        order.delivery_cost = 5.00
    elif form.cleaned_data['delivery_method'] == 'express':
        order.delivery_cost = 10.00
    elif form.cleaned_data['delivery_method'] == 'free' and cart.get_total_price() >= 100:  # Envío gratuito por compras >100€
        order.delivery_cost = 0.00
    else:
        order.delivery_cost = 5.00  # Predeterminado estándar si algo falla

    order.save()
    return order

def create_order_items(order, cart):
    for item in cart:
        OrderItem.objects.create(
            order=order,
            product=item['product'],
            price=item['price'],
            quantity=item['quantity']
        )


def process_stripe_payment(request, order):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': 'Pedido'},
                    'unit_amount': int(order.get_total_cost() * 100),
                },
                'quantity': 1,
            },
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('orders:order_created')) + f'?order_id={order.id}',
        cancel_url=request.build_absolute_uri(reverse('orders:order_create')),
    )
    send_confirmation_email(order)
    return redirect(session.url, code=303)


def process_cash_on_delivery(order):
    send_confirmation_email(order)
    return render(None, 'orders/order/created.html', {'order': order})


def send_confirmation_email(order):
    send_mail(
        'Confirmación de Pedido',
        f'''
        Tu pedido ha sido creado con éxito.

        ID de seguimiento: {order.tracking_id}
        Total: {order.get_total_cost()} €
        Dirección de entrega:
        {order.address}
        {order.postal_code}, {order.city}

        Gracias por tu compra.
        ''',
        settings.EMAIL_HOST_USER,
        [order.email],
        fail_silently=False,
    )


def order_track(request, tracking_id):
    order = get_object_or_404(Order, tracking_id=tracking_id)
    return render(request, 'orders/order/track.html', {'order': order})

def order_track_form(request):
    if request.method == 'POST':
        tracking_id = request.POST.get('tracking_id')
        try:
            order = get_object_or_404(Order, tracking_id=tracking_id)
            return redirect('orders:order_track', tracking_id=order.tracking_id)
        except:
            error_message = "No se encontró ningún pedido con el ID de seguimiento proporcionado."
            return render(request, 'orders/order/track_form.html', {'error': error_message})
    return render(request, 'orders/order/track_form.html')


def order_created(request):
    order_id = request.GET.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order/created.html', {'order': order})