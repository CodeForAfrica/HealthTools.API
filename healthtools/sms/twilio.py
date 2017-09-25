import logging
from flask import make_response


log = logging.getLogger(__name__)


def send_sms(msg, phone_no):
    response = '<?xml version="1.0" encoding="utf-8"?>' + \
               '<Response>' + \
               '<Message>' + msg + '</Message>' + \
               '</Response>'
    return response
