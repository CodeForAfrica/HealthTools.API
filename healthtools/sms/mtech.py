import logging
import requests

from flask import current_app


log = logging.getLogger(__name__)
SMS_SEND_URL = 'http://ke.mtechcomm.com/remote'


def send_sms(msg, phone_no):
    params = {
        'user': current_app.config.get('SMS_MTECH_USER'),
        'pass': current_app.config.get('SMS_MTECH_PASS'),
        'messageID': 0,
        'shortCode': current_app.config.get('SMS_MTECH_SHORTCODE'),
        'MSISDN': phone_no,
        'MESSAGE': msg
    }

    try:
        response = requests.get(SMS_SEND_URL, params=params).text
    except Exception as e:
        raise e

    return response
