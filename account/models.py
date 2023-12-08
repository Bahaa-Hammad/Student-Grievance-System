from __future__ import annotations
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

from django.contrib.auth.base_user import BaseUserManager


class AccountManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


class Department(models.Model):
    DEPARTMENT_CHOICES = (
    ('CAD', 'College of Art and Design'),
    ('CBA', 'College of Business Administration'),
    ('CCIS', 'College of Computer and Information Sciences'),
    ('CE', 'College of Engineering'),
    ('CHS', 'College of Health Sciences'),
    ('CL', 'College of Law'),
)
    name = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES)
    description = models.TextField()

    def __str__(self):
        return self.get_name_display()  # Returns the readable name for the department
    
class Account(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    email = models.EmailField(_("email address"), unique=True)
    first_name = models.CharField(max_length=20, blank=True, null=True)
    last_name = models.CharField(max_length=20, blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_student = models.BooleanField(default=False)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    date_joined = models.DateTimeField(default=timezone.now)
    reset_password = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    email_reset = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = AccountManager()

    class Meta:
        ordering = ['date_joined']

    def __str__(self):
        return self.email

    def create_student_account(email: str, password: str, first_name: str, last_name: str) -> Account:
            r'''
            creates an account object

            Parameters
            ---------
            email: str, password: str = None

            Return
            ---------
            account object
            '''
            try:
                if not email:
                    raise ValueError('Account must have an email address')
                email = Account.objects.normalize_email(email)
                account = Account.objects.create(email=email, first_name=first_name, last_name=last_name)
                account.set_password(password)
                account.is_active = False
                account.is_student = True
                account.save()
                account = Account.objects.get(email=email)
                return account
            except Exception as exception_message:
                return None, str(exception_message)
        
    def get_account(email: str):
        account = Account.objects.get(email=email)

        if account:
            return account
        return None

    def get_student_accounts():
        students = Account.objects.get(is_student=True)

        if students:
            return students
        return None

