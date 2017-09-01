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
from healthtools_ke_api.build_query import BuildQuery


SMS_SEND_URL = 'http://ke.mtechcomm.com/remote'
SMS_RESULT_COUNT = 4  # Number of results to be send via sms
DOC_KEYWORDS = ['doc', 'daktari', 'doctor', 'oncologist', 'dr']
CO_KEYWORDS = ['CO', 'clinical officer',
               'clinic officer', 'clinical', 'clinical oficer', ]
NO_KEYWORDS = ['nurse', 'no', 'nursing officer',
               'mhuguzi', 'muuguzi', 'RN', 'Registered Nurse']
NHIF_KEYWORDS = ['nhif', 'bima', 'insurance',
                 'insurance fund', 'health insurance', 'hospital fund']
HF_KEYWORDS = ['hf', 'hospital', 'dispensary', 'clinic',
               'hospitali', 'sanatorium', 'health centre']
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
