"""
Wit.ai will help predict the doc name the user is trying to search for. This will be based on how the 
wit will have been trained. 
wit.ai will be used when the query is made using /search?=<query>
"""

from wit import Wit 
from healthtools.search import elastic, nurses


access_token = "LHTGKRJ2VUYL52C2NTFEUZBQNCX7IVGO"

def determine_doc_type(query, doc_type=None):
    client = Wit(access_token = access_token)
    message_text = query
    resp = client.message(message_text)
    print(resp)
    query = resp['entities']['query']['value']
    doc_type = resp['entities'][0]
    return query, doc_type

def run_search(query, doc_type, search_type):
    if (search_type == 'nurses'):
        result = nurses.search(query)
    else:
        result = elastic.search(query, doc_type)
    return result

def run_query(query, doc_type=None):
    
    search_type = None

    doc_type, search_type = determine_doc_type(query, doc_type)

    # if (not doc_type):
    #     return False, False

    result = run_search(query, doc_type, search_type)

    return result, doc_type


