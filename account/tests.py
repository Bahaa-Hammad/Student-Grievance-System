from django.test import TestCase
from .models import Account
from .models import AccountManager
from .tokens import AccountActivationTokenGenerator, EmailResetToken
import six
# Create your tests here.


class AccountTest(TestCase):
    def setUp(self):
        account = Account.objects.create_user(email='student@psu.edu.sa', password="zsa", is_student=True)


    def test_get_account(self):
        Account.objects.get(email='student@psu.edu.sa')
        response = Account.get_account(email='student@psu.edu.sa')
        self.assertIsNotNone(response)

    def test_get_student_accounts(self):
        response = Account.get_student_accounts()
        self.assertIsNotNone(response)

    def test_make_hash_value(self):
        # Create a test user
        user = Account.objects.create(pk=1, email_confirmed=True)

        # Create an instance of YourUtilityClass (replace with your actual utility class)
        your_instance = AccountActivationTokenGenerator()

        # Set a timestamp for testing
        timestamp = 12345

        # Calculate the expected hash value
        expected_hash = (
            str(user.pk) + str(timestamp) +
            str(user.email_confirmed)
        )

        # Call the _make_hash_value method and compare the result with the expected value
        result = your_instance._make_hash_value(user, timestamp)
        self.assertEqual(result, expected_hash)
        

    def test_make_hash_value(self):
        # Create a user instance with necessary attributes
        user = Account(pk=1, email_reset="test@example.com")  # Replace with your actual user model

        # Create a timestamp
        timestamp = 12345

        # Calculate the expected hash value
        expected_hash = (
            six.text_type(user.pk) + six.text_type(user.email_reset) + six.text_type(timestamp)
        )

        # Call the _make_hash_value method
        your_instance = EmailResetToken()  # Create an instance of your model or class
        result = your_instance._make_hash_value(user, timestamp)

        # Compare the result with the expected value
        self.assertEqual(result, expected_hash)
        
