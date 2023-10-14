import requests
import json


def send_post_request(destination_url, payload):
    with open('apis/email/key.json', 'r') as newJsonFile:
        headers = json.loads(newJsonFile.read())

    response = requests.request("POST", destination_url, headers=headers, data=json.dumps(payload))
