from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Registro
    path('register/', views.register, name='register'),
    # Inicio de sesión
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # Cierre de sesión
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Perfil del usuario
    path('profile/', views.profile, name='profile'),
]
