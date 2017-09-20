import json


DOCUMENTS = {
    'doctors': {
        'search_type': 'elastic',
        'keywords': ['doc', 'daktari', 'doctor', 'oncologist', 'dr']
    },
    'clinical-officers': {
        'search_type': 'elastic',
        'keywords': ['CO', 'clinical officer', 'clinic officer', 'clinical',
                     'clinical oficer']
    },
    'nurses': {
        'search_type': 'nurses',
        'keywords': ['nurse', 'no', 'nursing officer', 'mhuguzi', 'muuguzi',
                     'RN', 'Registered Nurse']
    },
    'nhif': {
        'search_type': 'elastic',
        'keywords': ['nhif', 'bima', 'insurance', 'insurance fund',
                     'health insurance', 'hospital fund']
    },
    'health-facilities': {
        'search_type': 'elastic',
        'keywords': ['hf', 'hospital', 'dispensary', 'clinic', 'hospitali',
                     'sanatorium', 'health centre']
    },

}


def get_docs():
    return DOCUMENTS


def format_query(query):
    ''' Format query ready to determine the doc_type from keywords. '''
    query = query.replace('.', '').replace(',', '').lower().strip()
    return query


def determine_doc_type(query, doc_type=None):

    # Determine if doc_type exists
    if (doc_type and doc_exists(doc_type)):
        return doc_type, DOCUMENTS[doc_type]['search_type']

    # Determine doc_type from query
    query = format_query(query)
    for doc in DOCUMENTS:
        for keyword in DOCUMENTS[doc]['keywords']:
            if query.startswith(keyword):
                return doc, DOCUMENTS[doc]['search_type']

    return False, False


def doc_exists(doc_type):
    for doc in DOCUMENTS:
        if (doc == doc_type):
            return True
    return False


def remove_keywords(query):
    query = format_query(query)
    for doc in DOCUMENTS:
        for keyword in DOCUMENTS[doc]['keywords']:
            if query.startswith(keyword):
                return query.replace(keyword, '', 1)
    return query
