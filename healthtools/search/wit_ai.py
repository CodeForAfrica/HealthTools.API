"""
Wit.ai will help predict the doc name the user is trying to search for. 
This will be based on how the wit will have been trained. 
wit.ai will be used when the query is made using /search?=<query>
"""
from wit import Wit 
from nested_lookup import nested_lookup
from healthtools.search import elastic, nurses
from healthtools.settings import WIT_ACCESS_TOKEN
from healthtools.documents import doc_exists

def determine_doc_type(query, doc_type=None):
    """
    This returns the doc name and the query.
    The response will return 2 keys one being the doc name and the other query
    wit.ai will returns all hyphens as underscores. 
    """
    client = Wit(access_token=WIT_ACCESS_TOKEN)
    message_text = query
    resp = client.message(message_text)
    query = ''.join(nested_lookup('value', resp['entities']['query']))
    doc_type = ''.join([var for var in (resp['entities'].keys()) if var != 'query'])
    doc_type = doc_type.replace("_", "-") # changes underscore to hyphen
    return doc_type, query

def run_search(query, doc_type, search_type):
    """
    This searches for the query as per the search type found
    """
    if search_type == 'nurses':
        result = nurses.search(query)
    else:
        result = elastic.search(query, doc_type)
    return result

def wit_run_query(query, doc_type=None):
    doc_type, query = determine_doc_type(query, doc_type)
    if not doc_type:
        return False, False

    if doc_exists(doc_type) is True:
        search_type = doc_type
    else:
        search_type = None

    result = run_search(query, doc_type, search_type)

    return result, doc_type
