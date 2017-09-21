from healthtools.search import elastic, nurses
from healthtools.search.keywords import determine_doc_type, remove_keywords


def run_query(query, doc_type=None):

    search_type = None

    doc_type, search_type = determine_doc_type(query, doc_type)

    if (not doc_type):
        return False

    results = run_search(query, doc_type, search_type)

    return results


def run_search(query, doc_type, search_type):
    if (search_type == 'nurses'):
        results = nurses.search(remove_keywords(query))
    else:
        results = elastic.search(remove_keywords(query), doc_type)
    return results
