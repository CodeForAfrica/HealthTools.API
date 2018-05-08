import logging

from healthtools.sms import twilio, mtech
from healthtools.search import run_query

log = logging.getLogger(__name__)


def process_sms(args, adapter='mtech'):

    msg = args.get('message')
    phone_no = args.get('phoneNumber')

    if(adapter == 'twilio'):
        msg = args.get('Body')
        phone_no = args.get('From')

    # TODO: Track event SMS RECEIVED here

    result, doc_type = run_query(msg)

    sms_to_send = create_sms(result, doc_type)

    try:
        response = eval(adapter+'.send_sms(sms_to_send, phone_no)')
    except Exception as e:
        raise e

    if (adapter == 'twilio'):
        return response

    return {'msg': sms_to_send, 'phone_no': phone_no, 'response': response}


def create_sms(result, doc_type):
    '''
    Method to structure an SMS friendly response from
    search.run_query result.
    '''

    response = ''
    result_count = 1

    if (not result or not doc_type):
        log.info('No result')
        # TODO: Have this as a snippet in a txt file instead and import
        response = 'We could not understand your query. Try these:\n' + \
            '1. Doctors: DR. SAMUEL AMAI\n' + \
            '2. Clinical Officers: CO SAMUEL AMAI\n' + \
            '3. Nurses: NURSE SAMUEL AMAI\n' + \
            '4. NHIF Accredited hospital: NHIF KITALE\n' + \
            '5. Health Facility: HF KITALE'
        return response

    # TODO: Figure out singular vs plural
    response += 'Here are the top 3 matches your query returned'
    for hit in result['hits'][:3]:
        
        response += '\n' + '{}. {}'.format(str(result_count), hit['_source']['name'].encode('utf-8'))
        result_count += 1
    response += '\nFind the full list at http://health.the-star.co.ke/'
    log.info(response)
    return response
