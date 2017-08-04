# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..analytics import track_event
from ..elastic import Elastic
from .jsonify import jsonify
from ..settings import GA_TRACKING_ID


def index(request):
    '''
    Landing endpoint
    '''
    if request.method == 'GET':
        msg = {
            'name': 'API to Kenyan Clinical Officers registry',
            'authentication': [],
            'endpoints': {
                '/': {
                    'methods': ['GET']
                },
                '/clinical-officers/search.json': {
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
                    'data': {'clinical_officers': []}
                })

            # get clinical_officers by that name from aws
            response = {}
            es = Elastic()
            clinical_officers = es.get_from_elasticsearch('clinical-officers', query)

            if not clinical_officers:
                response['message'] = 'No clinical officer by that name found.'

            track_event(GA_TRACKING_ID,
                        'Clinical-Officers', 'search', request.META.get('REMOTE_ADDR'),
                        label=query, value=len(clinical_officers))
            response['data'] = {'clinical_officers': clinical_officers}
            response['status'] = 'success'

            results = jsonify(response, sort_keys=True)
            return results
        except Exception as err:
            return jsonify({
                'status': 'error',
                'message': str(err),
                'data': {'clinical_officers': []}
            })
