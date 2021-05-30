import requests
import json

import settings


def send_message(message):
    requests.post(settings.slack_url, data=json.dumps({
        'text' : message,
    }))
