from flask import Blueprint, request

from healthtools_ke_api.config import SMS_PASS, SMS_SHORTCODE, SMS_USER, GA_TRACKING_ID
from healthtools_ke_api.analytics import track_event

import requests
import re


SMS_SEND_URL = 'http://ke.mtechcomm.com/remote'
DOCTORS_SEARCH_URL = "https://6ujyvhcwe6.execute-api.eu-west-1.amazonaws.com/prod"
NURSE_SEARCH_URL = "https://api.healthtools.codeforafrica.org/nurses/search.json"
CO_SEARCH_URL = "https://vfblk3b8eh.execute-api.eu-west-1.amazonaws.com/prod"
NHIF_SEARCH_URL = "https://t875kgqahj.execute-api.eu-west-1.amazonaws.com/prod"
HF_SEARCH_URL = "https://187mzjvmpd.execute-api.eu-west-1.amazonaws.com/prod"
SMS_RESULT_COUNT = 4  # Number of results to be send via sms
DOC_KEYWORDS = ['doc', 'daktari', 'doctor', 'oncologist', 'dr']
CO_KEYWORDS = ['CO', 'clinical officer',
               'clinic officer', 'clinical', 'clinical oficer', ]
NO_KEYWORDS = ['nurse', 'no', 'nursing officer',
               'mhuguzi', 'RN', 'Registered Nurse']
NHIF_KEYWORDS = ['nhif', 'bima', 'insurance',
                 'insurance fund', 'health insurance', 'hospital fund']
HF_KEYWORDS = ['hf', 'hospital', 'dispensary', 'clinic',
               'hospitali', 'sanatorium', 'health centre']

sms_handler = Blueprint('sms_handler', __name__)


@sms_handler.route("/sms", methods=['GET'])
def sms():
    name = request.args.get("message")
    phone_number = request.args.get("phoneNumber")
    # Track Event SMS RECEIVED
    track_event(GA_TRACKING_ID, 'smsquery', 'receive',
                encode_cid(phone_number), label='lambda', value=2)
    msg = build_query_response(name)
    resp = send_sms(phone_number, msg[0])
    # Track Event SMS SENT
    track_event(GA_TRACKING_ID, 'smsquery', 'send',
                encode_cid(phone_number), label='lambda', value=2)
    # Full url with params for sending sms, print should trigger cloudwatch
    # log on aws
    print "SMS URL: ", resp.url
    # Response from the above url, print should trigger cloudwatch log on aws
    print "SMS PROVIDER RESPONSE", resp.text
    return msg[0]


def send_sms(phone_number, msg):
    params = {
        'user': SMS_USER,
        'pass': SMS_PASS,
        'messageID': 0,
        'shortCode': SMS_SHORTCODE,
        'MSISDN': phone_number,
        'MESSAGE': msg
    }
    resp = requests.get(SMS_SEND_URL, params=params)
    return resp


def find_keyword_in_query(query, keywords):
    regex = re.compile(r'\b(?:%s)\b' % '|'.join(keywords), re.IGNORECASE)
    return re.search(regex, query)


def build_query_response(query):
    query = clean_query(query)
    # Start by looking for doctors keywords
    if find_keyword_in_query(query, DOC_KEYWORDS):
        search_terms = find_keyword_in_query(query, DOC_KEYWORDS)
        query = query[:search_terms.start()] + query[search_terms.end():]
        r = requests.get(DOCTORS_SEARCH_URL, params={'q': query})
        msg = construct_docs_response(parse_cloud_search_results(r))
        print msg
        return [msg, r.json()]
    # Looking for Nurses keywords
    elif find_keyword_in_query(query, NO_KEYWORDS):
        search_terms = find_keyword_in_query(query, NO_KEYWORDS)
        query = query[:search_terms.start()] + query[search_terms.end():]
        r = requests.get(NURSE_SEARCH_URL, params={'q': query})
        print r.json()
        msg = construct_nurse_response(r.json()["data"]["nurses"][:SMS_RESULT_COUNT])
        print msg
        return [msg, r.json()]
    # Looking for clinical officers Keywords
    elif find_keyword_in_query(query, CO_KEYWORDS):
        search_terms = find_keyword_in_query(query, CO_KEYWORDS)
        query = query[:search_terms.start()] + query[search_terms.end():]
        r = requests.get(CO_SEARCH_URL, params={'q': query})
        msg = construct_co_response(parse_cloud_search_results(r))
        print msg
        return [msg, r.json()]
    # Looking for nhif hospitals
    elif find_keyword_in_query(query, NHIF_KEYWORDS):
        search_terms = find_keyword_in_query(query, NHIF_KEYWORDS)
        query = query[:search_terms.start()] + query[search_terms.end():]
        r = requests.get(NHIF_SEARCH_URL, params={'q': query})
        msg = construct_nhif_response(parse_cloud_search_results(r))
        print msg
        return [msg, r.json()]
    # Looking for health facilities
    elif find_keyword_in_query(query, HF_KEYWORDS):
        search_terms = find_keyword_in_query(query, HF_KEYWORDS)
        query = query[:search_terms.start()] + query[search_terms.end():]
        r = requests.get(HF_SEARCH_URL, params={'q': query})
        msg = construct_hf_response(parse_cloud_search_results(r))
        print msg
        return [msg, r.json()]
    # If we miss the keywords then reply with the prefered query formats
    else:
        msg_items = []
        msg_items.append("We could not understand your query. Try these:")
        msg_items.append("1. Doctors: DR. SAMUEL AMAI")
        msg_items.append("2. Clinical Officers: CO SAMUEL AMAI")
        msg_items.append("3. Nurses: NURSE SAMUEL AMAI")
        msg_items.append("4. NHIF accredited hospital: NHIF KITALE")
        msg_items.append("5. Health Facility: HF KITALE")
        msg = " ".join(msg_items)
        print msg
        return [msg, {'error': " ".join(msg_items)}]


def construct_co_response(co_list):
    # Just incase we found ourselves here with an empty list
    if len(co_list) < 1:
        return "Could not find a clinical officer with that name."
    count = 1
    msg_items = []
    for co in co_list:
        status = " ".join(
            [str(count) + ".", co['name'], "-", co['qualification']])
        msg_items.append(status)
        count = count + 1
    if len(co_list) > 1:
        msg_items.append("Find the full list at http://health.the-star.co.ke")
    print "\n".join(msg_items)
    return "\n".join(msg_items)


def construct_nhif_response(nhif_list):
    # Just incase we found ourselves here with an empty list
    if len(nhif_list) < 1:
        return "We could not find an NHIF accredited hospital in the location you provided."
    count = 1
    msg_items = []
    for nhif in nhif_list:
        status = " ".join([str(count) + ".", nhif['name']])
        msg_items.append(status)
        count = count + 1
    if len(nhif_list) > 1:
        msg_items.append("Find the full list at http://health.the-star.co.ke")

    return "\n".join(msg_items)


def construct_hf_response(hf_list):
    # Just incase we found ourselves here with an empty list
    if len(hf_list) < 1:
        return "We could not find a health facilty in the location you provided."
    count = 1
    msg_items = []
    for hf in hf_list:
        status = " ".join([str(count) + ".", hf['name'] +
                           " -", hf['keph_level_name']])
        msg_items.append(status)
        count = count + 1
    if len(hf_list) > 1:
        msg_items.append("Find the full list at http://health.the-star.co.ke")

    return "\n".join(msg_items)


def construct_nurse_response(nurse_list):
    # Just incase we found ourselves here with an empty list
    if len(nurse_list) < 1:
        return "Could not find a nurse with that name"
    count = 1
    msg_items = []
    for nurse in nurse_list:
        status = " ".join([str(count) + ".", nurse['name'] +
                           ",", "VALID TO", nurse['valid_till']])
        msg_items.append(status)
        count = count + 1
    if len(nurse_list) > 1:
        msg_items.append("Find the full list at http://health.the-star.co.ke")

    return "\n".join(msg_items)


def construct_docs_response(docs_list):
    # Just incase we found ourselves here with an empty list
    if len(docs_list) < 1:
        return "Could not find a doctor with that name"
    count = 1
    msg_items = []

    for doc in docs_list:
        # Ignore speciality if not there, dont display none
        if doc['specialty'] == "None":
            status = " ".join([str(count) + ".", doc['name'], "-",
                               doc['registration_number'], "-", doc['qualification']])
        else:
            status = " ".join([str(count) + ".", doc['name'], "-", doc[
                              'registration_number'], "-", doc['qualification'], doc['specialty']])
        msg_items.append(status)
        count = count + 1
    if len(docs_list) > 1:
        msg_items.append("Find the full list at http://health.the-star.co.ke")

    return "\n".join(msg_items)


def clean_query(query):
    query = query.lower().strip().replace(".", "")
    return query


def parse_cloud_search_results(response):
    result_to_send_count = SMS_RESULT_COUNT
    data_dict = response.json()
    fields_dict = (data_dict['hits'])
    hits = fields_dict['hit']
    result_list = []
    search_results_count = len(hits)
    print "FOUND {} RESULTS".format(search_results_count)
    for item in hits:
        result = item['fields']
        if len(result_list) < result_to_send_count:
            result_list.append(result)
        else:
            break
    return result_list


def encode_cid(phone_number):
    # TODO: Generate a hash instead of using phone number
    return phone_number
