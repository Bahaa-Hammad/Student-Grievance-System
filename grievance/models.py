import uuid
from django.db import models
from account.models import Account, Department


class Grievance(models.Model):
    STATUS = ((1, 'Solved'), (2, 'InProgress'), (3, 'Pending'))
    TYPE = (('ClassRoom', "Class Room"), ('Teacher', "Teacher"), ('Management', "Management"), ('Other', "Other"))

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey('account.Account', on_delete=models.CASCADE, default=None)

    subject = models.CharField(max_length=200, blank=False, null=True)
    type_of_complaint = models.CharField(choices=TYPE, null=True, max_length=200)
    description = models.TextField(max_length=4000, blank=False, null=True)
    date = models.DateField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=3)

    def __str__(self):
        return str(self.subject)

    def get_student_grievance(id, student: Account):
        grievance = Grievance.objects.get(id=id, student=student)

        if grievance:
            return grievance
        else:
            return None

    def get_student_grievances(student: Account):
        grievances = Grievance.objects.get(student=student)

        if grievances:
            return grievances
        else:
            return None

