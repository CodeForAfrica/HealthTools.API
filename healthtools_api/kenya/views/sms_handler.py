from nurses import get_nurses_from_nc_registry
from .errors import print_error
from .jsonify import jsonify
from ..analytics import track_event
from ..elastic import Elastic
from ..settings import GA_TRACKING_ID, SMS_USER, SMS_SHORTCODE, SMS_PASS

import requests
import re

SMS_SEND_URL = 'http://ke.mtechcomm.com/remote'
SMS_RESULT_COUNT = 4  # Number of results to be send via sms
DOC_KEYWORDS = ['doc', 'daktari', 'doctor', 'oncologist', 'dr']
CO_KEYWORDS = ['CO', 'clinical officer',
               'clinic officer', 'clinical', 'clinical oficer', ]
NO_KEYWORDS = ['nurse', 'no', 'nursing officer',
               'mhuguzi', 'muuguzi', 'RN', 'Registered Nurse']
NHIF_KEYWORDS = ['nhif', 'bima', 'insurance', 'civil', 'outpatient', 'inpatient',
                 'insurance fund', 'health insurance', 'hospital fund']
HF_KEYWORDS = ['hf', 'hospital', 'dispensary', 'clinic',
               'hospitali', 'sanatorium', 'health centre']
es = Elastic()


def sms(request):
    if request.method == 'GET':
        message = request.GET.get('message')
        phone_number = request.GET.get('phoneNumber')
        if not message or not phone_number:
            return jsonify("The url parameters 'message' and 'phoneNumber' are required.")
        # Track Event SMS RECEIVED
        track_event(GA_TRACKING_ID, 'smsquery', 'receive',
                    encode_cid(phone_number), label='lambda', value=2)
        msg = build_query_response(message)
        resp = send_sms(phone_number, msg[0])
        # Track Event SMS SENT
        track_event(GA_TRACKING_ID, 'smsquery', 'send',
                    encode_cid(phone_number), label='lambda', value=2)
        # Full url with params for sending sms, print should trigger cloudwatch
        # log on aws
        print 'SMS URL: ', resp.url
        # Response from the above url, print should trigger cloudwatch log on aws
        print 'SMS PROVIDER RESPONSE', resp.text
        return jsonify(msg[0], sort_keys= True)


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
        qry = query[:search_terms.start()] + query[search_terms.end():]
        doctors = es.get_from_elasticsearch('doctors', qry)
        msg = construct_docs_response(doctors[:SMS_RESULT_COUNT])
        check_message(msg)
        return [msg, 'doctors']  # return also the type for elastic search
    # Looking for Nurses keywords
    elif find_keyword_in_query(query, NO_KEYWORDS):
        search_terms = find_keyword_in_query(query, NO_KEYWORDS)
        qry = query[:search_terms.start()] + query[search_terms.end():]
        nurses = get_nurses_from_nc_registry(qry)
        msg = construct_nurse_response(nurses[:SMS_RESULT_COUNT])
        check_message(msg)
        return [msg, 'nurses']  # return also the type for elastic search
    # Looking for clinical officers Keywords
    elif find_keyword_in_query(query, CO_KEYWORDS):
        search_terms = find_keyword_in_query(query, CO_KEYWORDS)
        qry = query[:search_terms.start()] + query[search_terms.end():]
        clinical_officers = es.get_from_elasticsearch('clinical-officers', qry)
        msg = construct_co_response(clinical_officers[:SMS_RESULT_COUNT])
        check_message(msg)
        return [msg, 'clinical-officers']  # return also the type for elastic search
    # Looking for nhif hospitals
    elif find_keyword_in_query(query, NHIF_KEYWORDS):
        search_terms = find_keyword_in_query(query, NHIF_KEYWORDS)
        qry = query[:search_terms.start()] + query[search_terms.end():]
        if 'inpatient' in qry:
            nhif = es.get_from_elasticsearch('nhif-inpatient', qry)
        elif 'outpatient' in qry:
            nhif = es.get_from_elasticsearch('nhif-outpatient', qry)
        else:
            nhif = es.get_from_elasticsearch('nhif-outpatient-cs', qry)
        msg = construct_nhif_response(nhif[:SMS_RESULT_COUNT])
        check_message(msg)
        return [msg]
    # Looking for health facilities
    elif find_keyword_in_query(query, HF_KEYWORDS):
        search_terms = find_keyword_in_query(query, HF_KEYWORDS)
        qry = query[:search_terms.start()] + query[search_terms.end():]
        health_facilities = es.get_from_elasticsearch('health-facilities', qry)
        msg = construct_hf_response(health_facilities[:SMS_RESULT_COUNT])
        check_message(msg)
        return [msg, 'health-facilities']  # return also the type for elastic search
    # If we miss the keywords then reply with the preferred query formats
    else:
        print_error(query)
        msg_items = []
        msg_items.append('We could not understand your query. Try these:')
        msg_items.append('1. Doctors: DR. SAMUEL AMAI')
        msg_items.append('2. Clinical Officers: CO SAMUEL AMAI')
        msg_items.append('3. Nurses: NURSE SAMUEL AMAI')
        msg_items.append('4. NHIF accredited civil: NHIF KITALE')
        msg_items.append('5. NHIF accredited outpatient: NHIF KITALE')
        msg_items.append('6. NHIF accredited inpatient: NHIF KITALE')
        msg_items.append('7. Health Facility: HF KITALE')
        msg = ' '.join(msg_items)
        return [msg, {'error': ' '.join(msg_items)}]


def check_message(msg):
    # check the message and if query wasn't understood, post error
    if 'could not find' in msg:
        print_error(msg)

def construct_co_response(co_list):
    # Just incase we found ourselves here with an empty list
    if len(co_list) < 1:
        return 'Could not find a clinical officer with that name.'
    count = 1
    msg_items = []
    for co in co_list:
        co = co['fields']
        status = ' '.join(
            [str(count) + '.', ''.join(co['name']), '-', ''.join(co['qualifications'])])
        msg_items.append(status)
        count = count + 1
    if len(co_list) > 1:
        msg_items.append('Find the full list at http://health.the-star.co.ke')
    return '\n'.join(msg_items)


def construct_nhif_response(nhif_list):
    # Just incase we found ourselves here with an empty list
    if len(nhif_list) < 1:
        return 'Could not find an NHIF accredited hospital in the location you provided.'
    count = 1
    msg_items = []
    for nhif in nhif_list:
        status = ' '.join([str(count) + '.', nhif['name']])
        msg_items.append(status)
        count = count + 1
    if len(nhif_list) > 1:
        msg_items.append('Find the full list at http://health.the-star.co.ke')

    return '\n'.join(msg_items)


def construct_hf_response(hf_list):
    # Just incase we found ourselves here with an empty list
    if len(hf_list) < 1:
        return 'Could not find a health facility in the location you provided.'
    count = 1
    msg_items = []
    for hf in hf_list:
        status = ' '.join([str(count) + '.', hf['name'] +
                           ' -', hf['keph_level_name']])
        msg_items.append(status)
        count = count + 1
    if len(hf_list) > 1:
        msg_items.append('Find the full list at http://health.the-star.co.ke')

    return '\n'.join(msg_items)


def construct_nurse_response(nurse_list):
    # Just incase we found ourselves here with an empty list
    if len(nurse_list) < 1:
        return 'Could not find a nurse with that name'
    count = 1
    msg_items = []
    for nurse in nurse_list:
        status = ' '.join([str(count) + '.', nurse['name'] +
                           ',', 'VALID TO', nurse['valid_till']])
        msg_items.append(status)
        count = count + 1
    if len(nurse_list) > 1:
        msg_items.append('Find the full list at http://health.the-star.co.ke')

    return '\n'.join(msg_items)


def construct_docs_response(docs_list):
    # Just incase we found ourselves here with an empty list
    if len(docs_list) < 1:
        return 'Could not find a doctor with that name'
    count = 1
    msg_items = []

    for doc in docs_list:
        doc = doc['fields']
        # Ignore speciality if not there, dont display none
        if doc['speciality'] == 'None':
            status = ' '.join([str(count) + '.', ''.join(doc['name']), '-',
                               ''.join(doc['reg_no']), '-', ''.join(doc['qualifications'])])
        else:
            status = ' '.join([str(count) + '.', ''.join(doc['name']), '-', ''.join(doc[
                                                                                        'reg_no']), '-',
                               ''.join(doc['qualifications']), ''.join(doc['speciality'])])
        msg_items.append(status)
        count = count + 1
    if len(docs_list) > 1:
        msg_items.append('Find the full list at http://health.the-star.co.ke')

    return '\n'.join(msg_items)


def clean_query(query):
    query = query.lower().strip().replace('.', '')
    return query


def parse_elastic_search_results(response):
    result_to_send_count = SMS_RESULT_COUNT
    data_dict = response.json()
    fields_dict = (data_dict['hits'])
    hits = fields_dict['hit']
    result_list = []
    search_results_count = len(hits)
    print 'FOUND {} RESULTS'.format(search_results_count)
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
