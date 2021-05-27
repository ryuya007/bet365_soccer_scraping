import logging
import requests

import settings

logger = logging.getLogger(__name__)


def send_message(messages):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'Authorization': 'Bearer ' + settings.line_token}

    for message in messages:
        logger.info(message)
        payload = {'message': message}
        requests.post(url, headers=headers, params=payload,)
