from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('created/', views.order_created, name='order_created'),
]

urlpatterns += [
    path('track/<str:tracking_id>/', views.order_track, name='order_track'),
    path('track/', views.order_track_form, name='order_track_form'),
]