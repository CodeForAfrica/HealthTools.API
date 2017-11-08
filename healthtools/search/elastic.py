from healthtools.core import es, es_index, print_error


def search(query, doc_type):
    try:
        result = es.search(
            index=es_index,
            body={'query': match_all_text(query)},
            doc_type=doc_type
        )
        hits = result.get('hits', {})
        return hits
    except Exception as err:
        error = {
            "ERROR": "Elastic Search",
            "MESSAGE": str(err)
        }
        print_error(error)
    


def match_all():
    return {'match_all': {}}


def match_all_text(text):
    if text is None or not len(text.strip()):
        return match_all()
    return {
        'match': {
            '_all': {
                'query': text,
                'fuzziness': 1
            }
        }
    }
