"""
Wit.ai will help predict the doc name the user is trying to search for. This will be based on how the 
wit will have been trained. 
wit.ai will be used when the query is made using /search?=<query>
"""
import ast
import json

from wit import Wit 
from nested_lookup import nested_lookup
from healthtools.search import elastic, nurses
from settings import access_token

def determine_doc_type(query, doc_type=None):
    """
    This returns the doc name and the query.
    The response will return 2 keys one being the doc name and the othere query
    wit.ai returns all hyphens as underscores. 
    """
    client = Wit(access_token = access_token)
    message_text = query
    resp = client.message(message_text)
    query = ''.join(nested_lookup('value', resp['entities']['query']))
    doc_type = ''.join([var for var in (resp['entities'].keys()) if var != 'query'])
    doc_type = doc_type.replace("_", "-")
    return doc_type, query

def find_search_type(doc_type):
    """
    This checks the doc type against the doc list an determines whether it should be elastic search or nurses search.
    If the doc type is empty,search type is None 
    """
    doc = ['nhif-outpatient', 'nhif-inpatient', 'nhif-outpatient-cs', 'doctors', 'health-facilities', 'clinical-officers']
    if doc_type not in  doc:
        if doc_type is not 'nurses':
            search_type = None
        else:
            search_type = 'nurses'
    else:
        search_type = 'elastic'
    return search_type

def run_search(query, doc_type, search_type):
    """
    This searches for the query as per the search type found
    """
    if (search_type == 'nurses'):
        result = nurses.search(query)
    else:
        result = elastic.search(query, doc_type)
    return result

def run_query(query, doc_type=None):
    doc_type, query = determine_doc_type(query, doc_type)
    search_type = find_search_type(doc_type)
    if (not doc_type):
        return False, False

    result = run_search(query, doc_type, search_type)

    return result, doc_type


