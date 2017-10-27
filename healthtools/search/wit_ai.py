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
    doc = ''.join([var for var in (resp['entities'].keys()) if var != 'query'])
    doc = doc.replace("_", "-") # changes underscore to hyphen
    if doc_exists(doc) is True:
            doc = doc_type
    return doc_type, query

