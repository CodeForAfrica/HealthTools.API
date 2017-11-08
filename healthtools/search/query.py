from wit import Wit 
from nested_lookup import nested_lookup
from healthtools.settings import WIT_ACCESS_TOKEN

from healthtools.documents import DOCUMENTS, doc_exists
from healthtools.core import print_error

from healthtools.search import elastic, nurses


def run_query(query, doc_type=None):

    search_type = None

    if doc_type == 'wit':
        doc_type, query = determine_doc_type_using_wit(query)
    if doc_type is not 'nurses':
         search_type = 'elastic'
    else:
        search_type = 'nurses'
        return doc_type, search_type
    
    doc_type, search_type = determine_doc_type(query, doc_type)

    if not doc_type:
        return False, False

    result = run_search(query, doc_type, search_type)

    return result, doc_type


def run_search(query, doc_type, search_type):
    if search_type == 'nurses':
        result = nurses.search(remove_keywords(query))
    else:
        result = elastic.search(remove_keywords(query), doc_type)
    return result


def format_query(query):
    ''' Format query ready to determine the doc_type from keywords. '''
    query = query.replace('.', '').replace(',', '').lower().strip()
    return query


def determine_doc_type(query, doc_type=None):

    # Determine if doc_type exists
    if doc_type and doc_exists(doc_type):
        return doc_type, DOCUMENTS[doc_type]['search_type']

    # Determine doc_type from query
    query = format_query(query)
    for doc in DOCUMENTS:
        for keyword in DOCUMENTS[doc]['keywords']:
            if query.startswith(keyword + ' '):
                return doc, DOCUMENTS[doc]['search_type']
    error = {
        "ERROR": "doc_type could not be determined from query",
        "MESSAGE": 'Query supplied = ' + query
    }
    print_error(error)
    return False, False


def remove_keywords(query):
    query = format_query(query)
    for doc in DOCUMENTS:
        for keyword in DOCUMENTS[doc]['keywords']:
            if query.startswith(keyword + ' '):
                return query.replace(keyword, '', 1).strip()
    return query


"""
Wit.ai will help predict the doc name the user is trying to search for. 
This will be based on how the wit will have been trained. 
wit.ai will be used when the query is made using /search?=<query>
"""

def determine_doc_type_using_wit(query, doc_type=None):
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
    if doc_exists(doc_type) == True:
        return doc_type, query