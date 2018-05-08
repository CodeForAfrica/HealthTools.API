import logging
from healthtools.core import es, es_index

log = logging.getLogger(__name__)

def search(query, doc_type):
    if doc_type in ['doctors', 'doctors-foreign']:
        doc_type = 'doctors,doctors-foreign'
    
    try:
        result = es.search(
            index=es_index,
            body={'query': match_all_text(query)},
            doc_type=doc_type
        )
        
        hits = result.get('hits', {})
        return hits
    except Exception as err:
        log.error("Error fetching data from elastic search \n" + str(err))    


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
