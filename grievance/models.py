import uuid
from django.db import models
from account.models import Account


class Grievance(models.Model):
    STATUS = ((1, 'Solved'), (2, 'InProgress'), (3, 'Pending'))
    TYPE = (('ClassRoom', "Class Room"), ('Teacher', "Teacher"), ('Management', "Management"), ('Other', "Other"))

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    department = models.ManyToManyField('Department', blank=True)
    student = models.ForeignKey(Account, on_delete=models.CASCADE, default=None)

    subject = models.CharField(max_length=200, blank=False, null=True)
    type_of_complaint = models.CharField(choices=TYPE, null=True, max_length=200)
    description = models.TextField(max_length=4000, blank=False, null=True)
    date = models.DateField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=3)

    def __str__(self):
        return str(self.subject)


class Department(models.Model):
    TYPE = ((1, "CAD"), (2, "CBA"), (3, "CCIS"), (4, "CE"), (5, "CHS"), (6, "CL"))
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(choices=TYPE, max_length=200)

    def __str__(self):
        return self.name
