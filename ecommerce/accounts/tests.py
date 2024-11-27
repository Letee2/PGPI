from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AccountsTestCase(TestCase):
    def test_register_view(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_register_user(self):
        response = self.client.post(reverse('accounts:register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_login_view(self):
        user = User.objects.create_user(username='testuser', password='TestPassword123')
        response = self.client.post(reverse('accounts:login'), {
            'username': 'testuser',
            'password': 'TestPassword123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_profile_view_requires_login(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)  # Redirección al login

        user = User.objects.create_user(username='testuser', password='TestPassword123')
        self.client.login(username='testuser', password='TestPassword123')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
