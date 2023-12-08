from django.shortcuts import redirect, render
from account.models import Account
from grievance.models import Grievance
from .forms import LogInForm, AccountCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required



def register_student_account(request):
    form = AccountCreationForm()

    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            account = Account.create_student_account(email,password,first_name,last_name)

            if account:
                messages.success(request, 'Account was created!')
                login(request, account)
                return render(request, 'account/dashboard.html')
            else:
                messages.error(request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'account/register.html', context)


def login_account(request):

    # if request.user.is_authenticated:
    #     return redirect('dashboard')

    form = LogInForm()
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']

        account = authenticate(request, email=email, password=password)
        if account:
            login(request, account)
            return redirect(request.GET['next'] if 'next' in request.GET else 'dashboard')
        else:
            messages.error(request, 'Username OR password is incorrect')

    context = {'form': form}
    return render(request, 'account/login.html', context)


def logout_account(request):
    logout(request)
    messages.info(request, 'logged out!')
    return redirect('login')

@login_required(login_url='login')
def account_dashboard(request):
    student = request.user
    grievances = Grievance.get_student_grievances(student=student)
    context = {'grievances': grievances}
    return render(request, 'account/dashboard.html', context)