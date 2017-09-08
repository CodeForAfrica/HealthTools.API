import getpass
import json
import re
import requests

from datetime import datetime
from flask import Blueprint, request, current_app

from healthtools_ke_api.analytics import track_event
from healthtools_ke_api.settings import SLACK

from healthtools_ke_api.views.nurses import get_nurses_from_nc_registry
from healthtools_ke_api.elastic_search import Elastic
# from healthtools_ke_api.build_query import BuildQuery
from healthtools_ke_api.views.response import BuildQuery



SMS_SEND_URL = 'http://ke.mtechcomm.com/remote'

es = Elastic()
bq = BuildQuery()

sms_handler = Blueprint("sms_handler", __name__)


@sms_handler.route("/sms", methods=['GET'])
def sms():
    name = request.args.get("message")
    phone_number = request.args.get("phoneNumber")
    if not name or not phone_number:
        return "The url parameters 'message' and 'phoneNumber' are required."
    # Track Event SMS RECEIVED
    track_event(current_app.config.get('GA_TRACKING_ID'), 'smsquery', 'receive',
                encode_cid(phone_number), label='lambda', value=2)
    msg = bq.build_query_response(name)
    resp = send_sms(phone_number, msg[0])
    # Track Event SMS SENT
    track_event(current_app.config.get('GA_TRACKING_ID'), 'smsquery', 'send',
                encode_cid(phone_number), label='lambda', value=2)

    return msg[0]


def send_sms(phone_number, msg):
    params = {
        'user': current_app.config.get('SMS_USER'),
        'pass': current_app.config.get('SMS_PASS'),
        'messageID': 0,
        'shortCode': current_app.config.get('SMS_SHORTCODE'),
        'MSISDN': phone_number,
        'MESSAGE': msg
    }
    resp = requests.get(SMS_SEND_URL, params=params)
    return resp


def encode_cid(phone_number):
    # TODO: Generate a hash instead of using phone number
    return phone_number
