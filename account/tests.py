from django.test import TestCase
from .models import Account
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
