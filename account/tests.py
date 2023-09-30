from django.test import TestCase
from .models import Account
# Create your tests here.
class Account(TestCase):
    def setUp(self):
        account = Account.objects.create_user(email='student@psu.edu.sa')
        student = Account.objects.create_user(is_student=True)

    def test_get_account(self):
        account = Account.objects.all()[0]
        email = Account.objects.get(email='student@psu.edu.sa')
        response = Account.get_account(email='student@psu.edu.sa')
        self.assertIsNotNone(response)

    def test_get_student_accounts(self):
        student = Account.objects.all()[0]
        student = Account.object.get(is_student=True)
        self.assertIsNotNone(response)


