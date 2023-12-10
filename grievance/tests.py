from django.test import TestCase
from .models import Grievance, Department
from account.models import Account
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

class GrievanceModelTestCase(TestCase):

    def setUp(self):
        # Setup any necessary objects like a Department and a Student Account
        self.department = Department.objects.create(name='Test Department')
        self.student = Account.objects.create(email='student@example.com', password='testpass123')

    def test_create_grievance(self):
        # Create a Grievance instance
        grievance = Grievance.objects.create(
            department=self.department,
            student=self.student,
            subject='Test Subject',
            type_of_complaint=1,  # Assuming 1 corresponds to "Class Room"
            description='Test Description'
        )

        self.assertEqual(grievance.department, self.department)
        self.assertEqual(grievance.student, self.student)
        self.assertEqual(grievance.subject, 'Test Subject')
        self.assertEqual(grievance.type_of_complaint, 1)
        self.assertEqual(grievance.description, 'Test Description')
        self.assertEqual(grievance.status, 3)  # Default status is 'Pending'

    def test_grievance_string_representation(self):
        # If you have a __str__ method in your Grievance model
        grievance = Grievance.objects.create(
            department=self.department,
            student=self.student,
            subject='Test Subject',
            description='Test Description'
        )
        self.assertEqual(str(grievance), grievance.subject)


class GrievanceModelDefaultValueTestCase(TestCase):

    def setUp(self):
        self.department = Department.objects.create(name='Test Department')
        self.student = Account.objects.create(email='student@example.com', password='testpass123')

    def test_default_status(self):
        grievance = Grievance.objects.create(
            department=self.department,
            student=self.student,
            subject='Test Subject',
            description='Test Description'
        )
        self.assertEqual(grievance.status, 3)  # Assuming 3 is the default status for 'Pending'



class GrievanceCreationTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.department = Department.objects.create(name='Test Department')
        self.student = Account.objects.create_user(email='student@example.com', password='testpass123')

    def test_create_student_grievance(self):
        subject = 'Test Grievance'
        type_of_complaint = 1  # Assuming 1 corresponds to "Class Room"
        description = 'Test Description'

        grievance = Grievance.create_student_grievance(subject, type_of_complaint, self.department, description, self.student)

        self.assertIsNotNone(grievance)
        self.assertEqual(grievance.subject, subject)
        self.assertEqual(grievance.department, self.department)
        self.assertEqual(grievance.description, description)
        self.assertEqual(grievance.student, self.student)

class GrievanceRetrievalTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.department = Department.objects.create(name='Test Department')
        self.student = Account.objects.create_user(email='student@example.com', password='testpass123')
        self.grievance = Grievance.objects.create(subject='Test Grievance', type_of_complaint=1, department=self.department, description='Test Description', student=self.student)

    def test_get_student_grievance(self):
        retrieved_grievance = Grievance.get_student_grievance(self.grievance.id, self.student)
        self.assertIsNotNone(retrieved_grievance)
        self.assertEqual(retrieved_grievance, self.grievance)

class AllStudentGrievancesTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.department = Department.objects.create(name='Test Department')
        self.student = Account.objects.create_user(email='student@example.com', password='testpass123')
        Grievance.objects.create(subject='Test Grievance 1', type_of_complaint=1, department=self.department, description='Test Description 1', student=self.student)
        Grievance.objects.create(subject='Test Grievance 2', type_of_complaint=2, department=self.department, description='Test Description 2', student=self.student)

    def test_get_student_grievances(self):
        grievances = Grievance.get_student_grievances(self.student)
        self.assertEqual(grievances.count(), 2)


# Client Views

class SubmitGrievanceViewTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.client = Client()
        self.url = reverse('submit-grievance')
        self.user = User.objects.create_user(email='testuser@test.com', password='12345')
        self.department = Department.objects.create(name='Test Department')
        self.client.login(email='testuser@test.com', password='12345')

    def test_submit_grievance_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grievance/grievance-submission.html')

    def test_submit_grievance_POST_valid(self):
        grievance_data = {
            'subject': 'Test Subject',
            'type_of_complaint': 1,
            'department': self.department.id,
            'description': 'Test Description'
        }
        response = self.client.post(self.url, grievance_data)
        self.assertRedirects(response, reverse('dashboard'))
        # Verify that the grievance was created
        self.assertEqual(Grievance.objects.count(), 1)

    def test_submit_grievance_POST_invalid(self):
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grievance/grievance-submission.html')
        self.assertEqual(Grievance.objects.count(), 0)
        
class SubmittedGrievancesViewTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.client = Client()
        self.url = reverse('submited-grievances')
        self.user = User.objects.create_user(email='testuser@test.com', password='12345')
        self.client.login(email='testuser@test.com', password='12345')

    def test_submited_grievances_GET(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'grievance/submited_grievances.html')


class GrievanceViewTestCase(TestCase):

    def setUp(self):
        User = get_user_model()
        self.client = Client()
        self.user = User.objects.create_user(email='testuser@test.com', password='12345')
        self.department = Department.objects.create(name='Test Department')
        self.grievance = Grievance.objects.create(
            subject='Test Subject', 
            type_of_complaint=1, 
            department=self.department, 
            description='Test Description', 
            student=self.user
        )
        self.url = reverse('grievance', kwargs={'pk': self.grievance.id})
        self.client.login(username='testuser', password='12345')