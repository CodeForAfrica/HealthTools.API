from flask import Blueprint, request, current_app

from healthtools_ke_api.analytics import track_event
from healthtools_ke_api.views.nurses import get_nurses_from_nc_registry
from healthtools_ke_api.views.elastic_search import Elastic

import requests
import re

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

sms_handler = Blueprint("sms_handler", __name__)


@sms_handler.route("/sms", methods=['GET'])
def sms():
    '''
        This function sends an sms to a targeted phone number

        Query:
            message (str): The text to send
            phoneNumber (str): The phone number to send the sms to
        
        Returns:
            The message object
    '''

    name = request.args.get("message")
    phone_number = request.args.get("phoneNumber")
    if not name or not phone_number:
        return "The url parameters 'message' and 'phoneNumber' are required."
    # Track Event SMS RECEIVED
    track_event(current_app.config.get('GA_TRACKING_ID'), 'smsquery', 'receive',
                encode_cid(phone_number), label='lambda', value=2)
    msg = build_query_response(name)
    resp = send_sms(phone_number, msg[0])
    # Track Event SMS SENT
    track_event(current_app.config.get('GA_TRACKING_ID'), 'smsquery', 'send',
                encode_cid(phone_number), label='lambda', value=2)
    # Full url with params for sending sms, print should trigger cloudwatch
    # log on aws
    print "SMS URL: ", resp.url
    # Response from the above url, print should trigger cloudwatch log on aws
    # print "SMS PROVIDER RESPONSE", resp.text
    return msg[0]


def send_sms(phone_number, msg):
    '''
        This function sends sms 

        Args:
            message (str): The text to send
            phoneNumber (str): The phone number to send the sms to 

        Returns:
            The status  of the sms sent
    '''

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


def find_keyword_in_query(query, keywords):
    '''
        This function finds keyword in query

        Args:
            query(str): The string to lookup for keywords
            keywords(lst): The keywords to search

        Returns:
            A list of the keywords in query
    '''

    regex = re.compile(r'\b(?:%s)\b' % '|'.join(keywords), re.IGNORECASE)
    return re.search(regex, query)


def build_query_response(query):
    '''
        This function builds an sms object based on the query passed

        Args:
            query(str): Description of the User's request 

        Returns:
            json. The response can be any of the following ::

                When a keyword is found in the query
                    returns The sms object
                Else 
                    returns an error response with instances of  valid query
                        [
                            "We could not understand your query. Try these:",
                            "1. Doctors: DR. SAMUEL AMAI",
                            "2. Clinical Officers: CO SAMUEL AMAI",
                            "3. Nurses: NURSE SAMUEL AMAI",
                            "4. NHIF accredited hospital: NHIF KITALE",
                            "5. Health Facility: HF KITALE"
                        ]
            
    '''
    
    query = clean_query(query)
    # Start by looking for doctors keywords
    if find_keyword_in_query(query, DOC_KEYWORDS):
        search_terms = find_keyword_in_query(query, DOC_KEYWORDS)
        query = query[:search_terms.start()] + query[search_terms.end():]
        doctors = es.get_from_elasticsearch('doctors', query)
        msg = construct_docs_response(doctors[:SMS_RESULT_COUNT])
        return [msg]
    # Looking for Nurses keywords
    elif find_keyword_in_query(query, NO_KEYWORDS):
        search_terms = find_keyword_in_query(query, NO_KEYWORDS)
        query = query[:search_terms.start()] + query[search_terms.end():]
        nurses = get_nurses_from_nc_registry(query)
        msg = construct_nurse_response(nurses[:SMS_RESULT_COUNT])
        return [msg]
    # Looking for clinical officers Keywords
    elif find_keyword_in_query(query, CO_KEYWORDS):
        search_terms = find_keyword_in_query(query, CO_KEYWORDS)
        query = query[:search_terms.start()] + query[search_terms.end():]
        clinical_officers = es.get_from_elasticsearch('clinical-officers', query)
        msg = construct_co_response(clinical_officers[:SMS_RESULT_COUNT])
        return [msg]
    # Looking for nhif hospitals
    elif find_keyword_in_query(query, NHIF_KEYWORDS):
        search_terms = find_keyword_in_query(query, NHIF_KEYWORDS)
        query = query[:search_terms.start()] + query[search_terms.end():]
        nhif = es.get_from_elasticsearch('nhif-outpatient', query)
        msg = construct_nhif_response(nhif[:SMS_RESULT_COUNT])
        print msg
        return [msg]
    # Looking for health facilities
    elif find_keyword_in_query(query, HF_KEYWORDS):
        search_terms = find_keyword_in_query(query, HF_KEYWORDS)
        query = query[:search_terms.start()] + query[search_terms.end():]
        health_facilities = es.get_from_elasticsearch('health-facilities', query)
        msg = construct_hf_response(health_facilities[:SMS_RESULT_COUNT])
        print msg
        return [msg]
    # If we miss the keywords then reply with the preferred query formats
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
    '''
        This function builds dynamic message item for a list of clinical officers supplied by the user

        Args:
             co_list(list): The list of clinical officers
        
        Returns:
            json. The list of message items for clinical officers
    '''

    # Just incase we found ourselves here with an empty list
    if len(co_list) < 1:
        return "Could not find a clinical officer with that name."
    count = 1
    msg_items = []
    for co in co_list:
        co = co['_source']
        status = " ".join(
            [str(count) + ".", "".join(co['name']), "-", "".join(co['qualifications'])])
        msg_items.append(status)
        count = count + 1
    if len(co_list) > 1:
        msg_items.append("Find the full list at http://health.the-star.co.ke")
    print "\n".join(msg_items)
    return "\n".join(msg_items)


def construct_nhif_response(nhif_list):
    '''
        This function builds dynamic message item for a list of NHIF's supplied by the user

        Args:
             nhif_list(list): The list of NHIF's
        
        Returns:
            json. The list of message items for NHIF's
    '''

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
    '''
        This function builds dynamic message item for a list of HF's supplied by the user

        Args:
             hf_list(list): The list of HF's
        
        Returns:
            json. The list of message items for HF's
    '''

    # Just incase we found ourselves here with an empty list
    if len(hf_list) < 1:
        return "We could not find a health facility in the location you provided."
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
    '''
        This function builds dynamic message item for a list of nurses supplied by the user

        Args:
             nurse_list(list): The list of nurses
        
        Returns:
            json. The list of message items for nurses
    '''

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
    
    '''
        This function builds dynamic message item for a list of doctors supplied by the user

        Args:
             nurse_list(list): The list of doctors
        
        Returns:
            json. The list of message items for doctors
    '''

    # Just incase we found ourselves here with an empty list
    if len(docs_list) < 1:
        return "Could not find a doctor with that name."
    count = 1
    msg_items = []

    for doc in docs_list:
        # Ignore speciality if not there, dont display none
        doc = doc['_source']
        if doc['practice_type'] == "None":
            status = " ".join([str(count) + ".", "".join(doc['name']), "-",
                               "".join(doc['reg_no']), "-", "".join(doc['qualifications'])])
        else:
            status = " ".join([str(count) + ".", "".join(doc['name']), "-", "".join(doc[
                                                                                        'reg_no']), "-",
                               "".join(doc['qualifications']), "".join(doc['practice_type'])])
        msg_items.append(status)
        count = count + 1
    if len(docs_list) > 0:
        msg_items.append("Find the full list at http://health.the-star.co.ke")

    return "\n".join(msg_items)


def clean_query(query):
    '''
        This function removes whitespaces, fullstop mark

        Args:
            query(str): The owrd to clean
        Returns:
            str. The lowercase of the cleaned word
    '''


    query = query.lower().strip().replace(".", "")
    return query


def parse_elastic_search_results(response):
    '''
        This function builds a list of result set with size as specified in the config variable <SMS_RESULT_COUNT>

        Args:
            response(json):
                The search result
        Returns:
            The parsed list of response object
    '''

    result_to_send_count = SMS_RESULT_COUNT
    data_dict = response.json()
    fields_dict = (data_dict['hits'])
    hits = fields_dict['hit']
    result_list = []
    search_results_count = len(hits)
    print "FOUND {} RESULTS".format(search_results_count)
    for item in hits:
        result = item
        if len(result_list) < result_to_send_count:
            result_list.append(result)
        else:
            break
    return result_list


def encode_cid(phone_number):
    # TODO: Generate a hash instead of using phone number
    return phone_number
