from datetime import timezone
import uuid
from django.db import models
from django.forms import ValidationError
from account.models import Account, Department


class Grievance(models.Model):
    STATUS = ((1, 'Solved'), (2, 'In Progress'), (3, 'Pending'))
    TYPE = ((1, "Class Room"), (2, "Teacher"), (3, "Management"), (4, "Other"))

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey('account.Account', on_delete=models.CASCADE, default=None)

    subject = models.CharField(max_length=200, blank=False, null=True)
    type_of_complaint = models.CharField(choices=TYPE, null=True, blank=True,max_length=200)
    description = models.TextField(max_length=4000, blank=False, null=True)
    date = models.DateField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=3)
    
    def __str__(self):
        return str(self.subject)
    def create_student_grievance(subject, type_of_complaint, department, description, student):
        """
            Create a Grievance instance from form data.
            return: Grievance instance if successful, None otherwise
        """
        try:

            grievance = Grievance.objects.create(subject=subject, type_of_complaint=type_of_complaint,department=department, description=description, student=student)
            grievance.save()
            
            return grievance
        except (ValidationError, Exception) as e:
            return None

    def get_student_grievance(id, student: Account):
        grievance = Grievance.objects.get(id=id, student=student)

        if grievance:
            return grievance
        else:
            return None

    def get_student_grievances(student: Account):
        grievances = Grievance.objects.filter(student=student)

        if grievances:
            return grievances
        else:
            return None

class GrievanceNotification(models.Model):
    grievance = models.ForeignKey(Grievance, on_delete=models.CASCADE, related_name='notifications')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Notification for {self.grievance.subject}"

    