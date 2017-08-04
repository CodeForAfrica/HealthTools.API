import json
import memcache
import requests


from bs4 import BeautifulSoup

from .jsonify import jsonify
from ..analytics import track_event
from ..settings import MEMCACHED_URL, GA_TRACKING_ID


cache = memcache.Client([MEMCACHED_URL], debug=True)  # cache server

nurse_fields = ['name', 'licence_no', 'valid_till']
NURSING_COUNCIL_URL = 'http://nckenya.com/services/search.php?p=1&s={}'


def index(request):
    '''
    Landing endpoint
    '''
    if request.method == 'GET':
        msg = {
            'name': 'Nursing Council of Kenya API',
            'authentication': [],
            'endpoints': {
                '/': {'methods': ['GET']},
                '/nurses/search.json': {
                    'methods': ['GET'],
                    'args': {
                        'q': {'required': True}
                    }
                },
            }
        }
        return jsonify(msg, sort_keys=True)


def search(request):
    if request.method == 'GET':
        try:
            query = request.GET.get('q')
            if not query or len(query) < 1:
                return jsonify({
                    'error': 'A query is required.',
                    'results': '',
                    'data': {'nurses': []}
                    })

            # try to get queried result first
            cached_result = cache.get(query.replace(' ', ''))
            if cached_result:
                num_cached_results = len(json.loads(
                    cached_result.content)['data']['nurses'])
                track_event(GA_TRACKING_ID, 'Nurse', 'search',
                            request.META.get('REMOTE_ADDR'), label=query, value=num_cached_results)
                cached_result['X-Retrieved-From-Cache'] = True
                return cached_result

            # get nurses by that name from nursing council site
            response = {}
            nurses = get_nurses_from_nc_registry(query)
            if not nurses:
                response['message'] = 'No nurse by that name found.'

            # send action to google analytics
            track_event(GA_TRACKING_ID,
                        'Nurse', 'search',
                        request.META.get('REMOTE_ADDR'), label=query, value=len(nurses))

            response['data'] = {'nurses': nurses}
            response['status'] = 'success'

            results = jsonify(response, sort_keys=True)
            cache.set(query.replace(' ', ''), results,
                      time=345600)  # expire after 4 days
            return results

        except Exception as err:
            return jsonify({
                'status': 'error',
                'message': str(err),
                'data': {'nurses': []}
            })


def get_nurses_from_nc_registry(query):
    '''
    Get nurses from the nursing council of Kenya registry
    '''
    url = NURSING_COUNCIL_URL.format(query)
    response = requests.get(url)
    nurses = []

    if 'No results' in response.content:
        return nurses

    # make soup for parsing out of response and get the table
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'class': 'zebra'}).find('tbody')
    rows = table.find_all('tr')

    # parse table for the nurses data
    for row in rows:
        # only the columns we want
        columns = row.find_all('td')[:len(nurse_fields)]
        columns = [text.text.strip() for text in columns]

        entry = dict(zip(nurse_fields, columns))
        nurses.append(entry)

    return nurses
