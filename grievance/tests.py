from django.test import TestCase
from .models import Grievance

from account.models import Account


class GrievanceTest(TestCase):

    def setUp(self):
        student = Account.objects.create_user(email='student@psu.edu.sa', password='xyz', is_student=True)
        Grievance.objects.create(subject="class", description="class AC", type_of_complaint="Teacher", student=student)

    def test_get_student_grievance(self):
        grievance = Grievance.objects.all()[0]
        student = Account.objects.get(email='student@psu.edu.sa')
        response = Grievance.get_student_grievance(id=grievance.id, student=student)
        # Return type:
        self.assertIsNotNone(response)
