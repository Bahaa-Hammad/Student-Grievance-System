from django.test import TestCase, Client
from .models import Account, Department
from django.core.exceptions import ValidationError



from django.urls import reverse
from django.contrib.auth import get_user_model


class AccountManagerTestCase(TestCase):

    def test_create_user(self):
        user = Account.objects.create_user(email='user@example.com', password='testpass123')
        self.assertEqual(user.email, 'user@example.com')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

    def test_create_user_with_no_email(self):
        with self.assertRaises(ValueError):
            Account.objects.create_user(email='', password='testpass123')

    def test_create_superuser(self):
        admin_user = Account.objects.create_superuser(email='admin@example.com', password='adminpass123')
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_staff)

    def test_create_superuser_with_wrong_flag(self):
        with self.assertRaises(ValueError):
            Account.objects.create_superuser(email='admin@example.com', password='adminpass123', is_staff=False)

class AccountModelTestCase(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(email='user@example.com', password='testpass123')

    def test_uidb64(self):
        encoded_email = self.user.uidb64
        self.assertIsInstance(encoded_email, str)

    def test_uidb64_to_email(self):
        encoded_email = self.user.uidb64
        decoded_email = Account.uidb64_to_email(encoded_email)
        self.assertEqual(decoded_email, 'user@example.com')



class AccountActivationTestCase(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user(email='user2@example.com', password='testpass456', is_active=False)

    def test_activate_account(self):
        self.assertFalse(self.user.is_active)
        activation_result = self.user.activate_account()
        self.assertTrue(activation_result)
        self.assertTrue(self.user.is_active)

    def test_reset_sent_emails(self):
        self.user.sent_emails = 5
        self.user.save()
        reset_result = self.user.reset_sent_emails()
        self.assertTrue(reset_result)
        self.assertEqual(self.user.sent_emails, 0)


# Client Views Testing
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class RegisterStudentAccountTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.url = reverse('register')

    def test_redirect_if_authenticated(self):
        # Create and login a user
        User = get_user_model()
        user = User.objects.create_user('test@example.com', 'password')
        self.client.login(email='test@example.com', password='password')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('dashboard'))

    def test_register_form_displayed(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/register.html')

    def test_valid_register_post_request(self):
        
        response = self.client.post(self.url, {'email': 'newuser@example.com', 'password1': 'testpass123', 'password2': 'testpass123', 'first_name': 'Test', 'last_name': 'User'})
        self.assertRedirects(response, reverse('verify-account', kwargs={'uidb64': 'bmV3dXNlckBleGFtcGxlLmNvbQ=='}))
        

class LogoutAccountTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('logout')

    def test_logout(self):
        # Assume user is logged in here
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('login'))
        

class VerifyAccountTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.url = reverse('verify-account', kwargs={'uidb64': 'bmV3dXNlckBleGFtcGxlLmNvbQ=='}) 

    def test_redirect_if_authenticated(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('dashboard'))
        

class ActivateAccountTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(email='testuser@example.com', password='password123')
        self.url = reverse('activate-account', kwargs={'uidb64': 'user_uidb64', 'token': 'account_token'})  # Replace with appropriate uidb64 and token

    def test_redirect_if_authenticated(self):
        self.client.login(email='testuser@example.com', password='password123')
        response = self.client.get(self.url)
        self.assertRedirects(response, reverse('dashboard'))