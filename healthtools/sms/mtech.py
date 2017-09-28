import logging
import requests

from flask import current_app


log = logging.getLogger(__name__)

SMS_SEND_URL = 'http://ke.mtechcomm.com/bulkAPIV2/'


def send_sms(msg, phone_no):
    params = {
        'User': current_app.config.get('SMS_MTECH_USER'),
        'Pass': current_app.config.get('SMS_MTECH_PASS'),
        'shortCode': current_app.config.get('SMS_MTECH_SHORTCODE'),
        'MSISDN': phone_no,
        'MESSAGE': msg,
        'logMessage': 0  # Needed for line break
    }

    try:
        response = requests.get(SMS_SEND_URL, params=params).text
    except Exception as e:
        raise e

    return response
