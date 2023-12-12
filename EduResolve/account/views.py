from django.shortcuts import redirect, render
from account.models import Account
from grievance.models import Grievance
from .forms import LogInForm, AccountCreationForm
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .utility import get_action_url, send_verification_email


def register_student_account(request):
    
    if request.user.is_authenticated:
        return redirect('dashboard')
    
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
                return redirect('verify-account', uidb64=account.uidb64)
            else:
                messages.error(request, 'An error has occurred during registration')

    context = {'form': form}
    return render(request, 'account/register.html', context)


def login_account(request):
    
    if request.user.is_authenticated:
        return redirect('dashboard')

    form = LogInForm()
    if request.method == 'POST':
        email = request.POST['email'].lower()
        password = request.POST['password']

        account = Account.get_account(email=email)
        if account:

            if not account.email_confirmed:
                return redirect('verify-account', uidb64=account.uidb64)
                
        authenticated_account = authenticate(request, email=email, password=password)
        
        if authenticated_account:
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


# Account Verfication & Activation

def verify_account(request, uidb64):
    '''Verifies an account through tokens'''

    if request.user.is_authenticated:
        return redirect('dashboard')

    email = Account.uidb64_to_email(uidb64)
    account = Account.get_account(email=email)

    if not account:
        return render(request, 'account/404.html', status=404)

    # Sending token to account's email
    token = account.get_activation_token()
    action = 'activate-account'
    activation_url = get_action_url(request, action, uidb64, token)

    if request.method == 'POST' and account.sent_emails >= 0:
        send_verification_email(request, account, activation_url, email)

    # Only for newly created accounts
    if request.method == 'GET' and account.sent_emails == 0:
        send_verification_email(request, account, activation_url, email)

    context = {'email': email}
    return render(request, 'account/verify-account.html', context)


def activate_account(request, uidb64, token):
    '''Activates account if the sent token is valid'''

    if request.user.is_authenticated:
        return redirect('dashboard')

    account = Account.check_activation_token(uidb64, token)

    if account:
        account.activate_account()
        account.reset_sent_emails()
        return render(request, 'account/activated.html')

    return render(request, 'account/404.html', status=404)