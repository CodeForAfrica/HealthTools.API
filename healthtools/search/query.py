import logging
from wit import Wit 
from nested_lookup import nested_lookup
from healthtools.settings import WIT_ACCESS_TOKEN

from healthtools.documents import DOCUMENTS, doc_exists
from healthtools.search import elastic, nurses, clinicalofficers

log = logging.getLogger(__name__)

def run_query(query, doc_type=None, page=1, per_page=10):

    doc_type, search_type = determine_doc_type(query, doc_type)

    if not doc_type:
        return False, False

    result = run_search(query, doc_type, search_type, page, per_page)

    return result, doc_type


def run_search(query, doc_type, search_type, page, per_page):
    if search_type == 'nurses':
        result = nurses.search(remove_keywords(query))
    elif search_type == 'clinicalofficers':
        result = clinicalofficers.search(remove_keywords(query))
    else:
        result = elastic.search(remove_keywords(query), doc_type, page, per_page)
    return result


def format_query(query):
    ''' Format query ready to determine the doc_type from keywords. '''
    query = query.replace('.', '').replace(',', '').lower().strip()
    return query


def determine_doc_type(query, doc_type=None):

    # Determine if doc_type exists
    if doc_type and doc_exists(doc_type):
        return doc_type, DOCUMENTS[doc_type]['search_type']
    
    # Is doc_type to trying to use wit?
    if doc_type == 'wit':
        return determine_doc_type_using_wit(query)

    # Determine doc_type from query
    query = format_query(query)
    for doc in DOCUMENTS:
        for keyword in DOCUMENTS[doc]['keywords']:
            if query.startswith(keyword + ' '):
                return doc, DOCUMENTS[doc]['search_type']
    log.error("doc_type could not be determined from query\n Query: " + query)
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
    doc_type = ''.join([var for var in (list(resp['entities'].keys())) if var != 'query'])
    doc_type = doc_type.replace("_", "-") # changes underscore to hyphen
    if doc_exists(doc_type) == True:
        return doc_type, query