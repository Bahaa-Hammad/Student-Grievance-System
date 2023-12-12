from __future__ import annotations
from .models import Account
from student_grievance_system.settings import DEBUG as devolopment_mode
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import reverse
from apis.postmark.handler import send_post_request


def get_action_url(request, action: str, uidb64: str, token: str, next: str = None) -> str:
    '''
        Creates URL to be sent via email
        Parameters
        ---------
        request, action: str, email: str, token: str
        Return
        ---------
        Action based URL
    '''
    if devolopment_mode:
        protocol = "http"
    else:
        protocol = "https"

    domain = get_current_site(request)

    path = reverse(action, kwargs={'uidb64': uidb64, 'token': token})
    action_url = f"{protocol}://{domain}{path}"

    if next:
        action_url += next

    return action_url


def send_verification_email(request, account: Account, action_url: str, receiver: str) -> bool:
    r'''
    Sends an emai via Postmark API
    Parameters
    ---------
    request, self: Account , template_alias: str , action_url: str , receiver: str
    Return
    ---------
    If the email is sent, returns True
    '''


    payload = {
        "From": "EduResolve@kuthbanhosting.com",
        "To": receiver,
        "TemplateAlias": 'activate-account',
        "TemplateModel": {
            "product_name": "EduResolve",
            "company_name": "EduResolve",
            "company_address": "Saudi Arabia, Riyadh",
            "name": receiver.split("@")[0],
            "action_url": action_url,
        },
    }
    send_post_request('https://api.postmarkapp.com/email/withTemplate', payload)
    account.sent_emails += 1
    account.save()