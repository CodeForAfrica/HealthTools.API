import logging

from healthtools.sms import twilio, mtech
from healthtools.documents import DOCUMENTS

log = logging.getLogger(__name__)


def process_sms(args, adapter='mtech'):
    result = {}

    try:
        result = eval(adapter+'.process_sms(args)')
    except Exception as e:
        raise e

    return result


def create_sms(result, doc_type):
    '''
    Method to structure an SMS friendly response from
    search.run_query result.
    '''

    response = ''

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
    response += 'We found ' + str(result['total']) + ' matches:'
    for hit in result['hits'][:3]:
        response += '\n' + hit['_source']['name']

    return response
