from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Profile

User = get_user_model()

class AccountsTests(TestCase):

    def setUp(self):
        # Crear un usuario
        self.user = User.objects.create_user(
            email='testuser@example.com',
            password='TestPassword123'
        )
        # Recuperar el perfil asociado automáticamente
        self.profile = self.user.profile
        self.profile.address = '123 Test St'
        self.profile.postal_code = '12345'
        self.profile.city = 'Test City'
        self.profile.save()

    def test_register_view_get(self):
        """Probar que la vista de registro carga correctamente"""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_register_view_post_valid_data(self):
        """Probar que el formulario de registro funciona con datos válidos"""
        response = self.client.post(reverse('accounts:register'), {
            'email': 'newuser@example.com',
            'password1': 'NewPassword123',
            'password2': 'NewPassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:login'))
        self.assertTrue(User.objects.filter(email='newuser@example.com').exists())

    def test_register_view_post_invalid_data(self):
        """Probar que el formulario de registro falla con datos inválidos"""
        response = self.client.post(reverse('accounts:register'), {
            'email': 'newuser@example.com',
            'password1': 'short',
            'password2': 'short',
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/register.html')
        self.assertFalse(User.objects.filter(email='newuser@example.com').exists())

    def test_profile_view_get_authenticated_user(self):
        """Probar que la vista de perfil carga correctamente para un usuario autenticado"""
        self.client.login(email='testuser@example.com', password='TestPassword123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/profile.html')
        self.assertContains(response, self.profile.address)

    def test_profile_view_post_update_profile(self):
        """Probar que un usuario autenticado puede actualizar su perfil"""
        self.client.login(email='testuser@example.com', password='TestPassword123')
        response = self.client.post(reverse('accounts:profile'), {
            'address': '456 New Address',
            'postal_code': '54321',
            'city': 'New City',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('accounts:profile'))
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.address, '456 New Address')
        self.assertEqual(self.profile.postal_code, '54321')
        self.assertEqual(self.profile.city, 'New City')

    def test_profile_view_redirect_unauthenticated_user(self):
        """Probar que los usuarios no autenticados son redirigidos al iniciar sesión"""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={reverse('accounts:profile')}")
