from django.test import TestCase
from .models import Account
from .models import AccountManager
# Create your tests here.


class AccountTest(TestCase):
    def setUp(self):
        account = Account.objects.create_user(email='student@psu.edu.sa', password="zsa", is_student=True)

    def test_get_account(self):
        Account.objects.get(email='student@psu.edu.sa')
        response = Account.get_account(email='student@psu.edu.sa')
        self.assertIsNotNone(response)

    def test_get_student_accounts(self):
<<<<<<< HEAD
        response = Account.get_student_accounts()
        self.assertIsNotNone(response)
=======
        student = Account.objects.all()[student]
        student = Account.object.get(is_student=True)
        self.assertIsNotNone(response)

    def test_create_user(self):
        student = AccountManager.object.create_user(email='student@psu.edu.sa', password='xyz')
        self.assertEqual(user.email, 'student@psu.edu.sa')
        self.assertTrue(user.check_password("xyz"))

    def test_create_superuser(self):
        admin = Account.objects.create_superuser(email='admin@psu.edu.sa', password='wasd')
        self.assertEqual(admin.email, 'admin@psu.edu.sa')
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)


    



    


>>>>>>> 47f4d1fa7a26af0f6334ab8e66f392f9c1150e17
