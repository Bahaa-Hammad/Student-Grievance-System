from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Account, Department


class AccountCreationForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)


    first_name.widget.attrs.update({'class': 'form-control form-control-lg'})
    last_name.widget.attrs.update({'class': 'form-control form-control-lg'})
    email.widget.attrs.update({'class': 'form-control form-control-lg'})
    password1.widget.attrs.update({'class': 'form-control form-control-lg'})
    password2.widget.attrs.update({'class': 'form-control form-control-lg'})

    class Meta:
        model = Account
        fields = ['first_name', 'last_name','email','password1', 'password2']


class LogInForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    email.widget.attrs.update({'class': 'form-control form-control-lg '})
    password.widget.attrs.update({'class': 'form-control form-control-lg'})

    class Meta:
        fields = [
            'email',
            'password',
        ]