from __future__ import annotations
from base64 import urlsafe_b64decode, urlsafe_b64encode
import base64
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import uuid

from django.contrib.auth.base_user import BaseUserManager
from .tokens import account_activation_token


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
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    reset_password = models.BooleanField(default=False)
    email_confirmed = models.BooleanField(default=False)
    email_reset = models.BooleanField(default=False)
    sent_emails = models.IntegerField(default=0)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = AccountManager()

    class Meta:
        ordering = ['date_joined']

    def __str__(self):
        return self.email
    
    @property
    def uidb64(self: Account) -> str:
        r'''Convert account email to base64 string and return it'''
        return base64.urlsafe_b64encode(self.email.encode()).decode()

    def uidb64_to_email(uidb64) -> str:
        r'''Convert base64 to email string and return it'''
        try:
            byte_str  = base64.urlsafe_b64decode(uidb64)
            email = byte_str.decode('utf-8')
            return email
        except Exception as e:
            # Handle exceptions (like decoding errors)
            return f"Error: {e}"
    
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

    def get_activation_token(self) -> str:
            r'''
            Creates activation token for an account

            Return
            ---------
            Account activation token & success message
            '''
            try:
                token = account_activation_token.make_token(self)
                return token
            except (Exception, TypeError, ValueError, OverflowError) as exception_message:
                return None, str(exception_message)

    def check_activation_token(uidb64: str, token: str) -> Account:
        r'''
        Checks the activation token sent via mail

        Parameters
        ---------
        uidb64: str , token: str

        Return
        ---------
        If the given token matches the account's: Account
        '''
        try:
            email = Account.uidb64_to_email(uidb64)
            account = Account.get_account(email)
            if not account:
                return None

            token_check_result = account_activation_token.check_token(account, token)
            
            if token_check_result:
                return account
            else:
                return None

        except (Exception, TypeError, ValueError, OverflowError):
            return None
    
    def activate_account(self) -> bool:
        r'''
        Activates an account

        Parameters
        ---------
        self: Account

        Return
        ---------
        True
        '''
        self.is_active = True
        self.email_confirmed = True  # True: The token link is invalid
        try:
            self.save()
            return True
        except (Exception) as exception_message:
            return False, str(exception_message)
        
    def reset_sent_emails(self) -> bool:
        r'''
        Resets number of sets emails to zero

        Parameters
        ---------
        self: Account

        Return
        ---------
        If emails reset succesfully, True & Success message 
        '''
        self.sent_emails = 0
        try:
            self.save()
            return True
        except (Exception) as exception_message:
            return False, str(exception_message)