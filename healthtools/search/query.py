from healthtools.documents import DOCUMENTS, doc_exists

from healthtools.search import elastic, nurses


def run_query(query, doc_type=None):

    search_type = None

    doc_type, search_type = determine_doc_type(query, doc_type)

    if (not doc_type):
        return False, False

    result = run_search(query, doc_type, search_type)

    return result, doc_type


def run_search(query, doc_type, search_type):
    if (search_type == 'nurses'):
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
    if (doc_type and doc_exists(doc_type)):
        return doc_type, DOCUMENTS[doc_type]['search_type']

    #Determine doc_type from query
    query = format_query(query)
    for doc in DOCUMENTS:
        for keyword in DOCUMENTS[doc]['keywords']:
            if query.startswith(keyword + ' '):
                return doc, DOCUMENTS[doc]['search_type']
            
    return False, False

def remove_keywords(query):
    query = format_query(query)
    for doc in DOCUMENTS:
        for keyword in DOCUMENTS[doc]['keywords']:
            if query.startswith(keyword + ' '):
                return query.replace(keyword, '', 1).strip()
    return query
