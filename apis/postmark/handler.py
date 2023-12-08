from account.models import Account
import requests
import json

def send_notification_email(request, receiver: str, message: str) -> bool:
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
        "name": receiver.split("@")[0],
        "HtmlBody": message

    }
    send_post_request('https://api.postmarkapp.com/email', payload)
    
def send_post_request(destination_url, payload):
    with open('apis/postmark/key.json', 'r') as newJsonFile:
        headers = json.loads(newJsonFile.read())

    response = requests.request("POST", destination_url, headers=headers, data=json.dumps(payload))
