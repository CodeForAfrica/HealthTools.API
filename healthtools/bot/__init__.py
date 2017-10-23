"""
This bot processor queries for the query sent as a message
can be used with wit.ai by changing the run query being used to wit_run_query function
"""
from healthtools.search import run_query

def process_bot_query(query):
    "Method to call run query fucntion that will search the entry on elastic search"
    
    result, doc_type = run_query(query)
    print result, doc_type

    reply_to_send = create_response(result, doc_type)
    return reply_to_send

def create_response(result, doc_type):
    '''
    Method to structure a bot friendly response
    '''
    response = ''
    if not result or not doc_type:
        response = 'We could not understand your query. Try these:\n' + \
            '1. Doctors: DR. SAMUEL AMAI\n' + \
            '2. Clinical Officers: CO SAMUEL AMAI\n' + \
            '3. Nurses: NURSE SAMUEL AMAI\n' + \
            '4. NHIF OUTPATIENT Accredited hospital: NHIF OUTPATIENT KITALE\n' + \
            '5. NHIF INPATIENT Accredited hospital: NHIF INPATIENT KAKAMEGA\n' + \
            '6. NHIF OUTPATIENT CS Accredited hospital: NHIF OUTPATIENT CS MOMBASA\n' + \
            '7. Health Facility: HF KITALE'
        return response

    response += 'This are the top 3 of the ' + str(result['total']) + ' matches found:' + '\n'
    for hit in result['hits'][:3]:
        response += '\n' + hit['_source']['name'] + '\n'
    return response + '\n' + 'visit https://health.the-star.co.ke/ to view more'
