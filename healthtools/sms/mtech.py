import logging
import requests

from flask import current_app

from healthtools.search import run_query


log = logging.getLogger(__name__)
SMS_SEND_URL = 'http://ke.mtechcomm.com/remote'


def process_sms(args):
    msg = args.get('message')
    phone_no = args.get('phoneNumber')

    # TODO: Track event SMS RECEIVED here

    result, doc_type = run_query(msg)

    # TODO: Find fix not to do the import here..
    from healthtools.sms import create_sms
    sms_to_send = create_sms(result, doc_type)

    response = send_sms(sms_to_send, phone_no)

    # TODO: Track event SMS SENT

    return {'msg': sms_to_send, 'phone_no': phone_no, 'response': ''}


def send_sms(msg, phone_no):
    params = {
        'user': current_app.config.get('HTOOLS_SMS_MTECH_USER'),
        'pass': current_app.config.get('HTOOLS_SMS_MTECH_PASS'),
        'messageID': 0,
        'shortCode': current_app.config.get('HTOOLS_SMS_MTECH_SHORTCODE'),
        'MSISDN': phone_no,
        'MESSAGE': msg
    }

    try:
        response = requests.get(SMS_SEND_URL, params=params)
    except Exception as e:
        raise e

    return response
