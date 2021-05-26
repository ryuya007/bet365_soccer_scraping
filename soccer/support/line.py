import requests

import settings


def send_message(messages):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + settings.line_token}

    # messages = ['Write your message']

    for message in messages:
        payload = {'message': message}
        requests.post(url, headers=headers, params=payload,)
