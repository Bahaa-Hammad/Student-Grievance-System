from django.shortcuts import redirect, render

from account.models import Account
from .forms import LogInForm, AccountCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required



def register_student_account(request):
    form = AccountCreationForm()

    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.is_student = True
            account.save()
            messages.success(request, 'Account was created!')
            login(request, account)
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
    print(request.user)
    context = {'null': 'null'}
    return render(request, 'account/dashboard.html', context)