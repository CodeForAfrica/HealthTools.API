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
            'name': 'API to Kenyan Health Facilities registry',
            'authentication': [],
            'endpoints': {
                '/': {
                    'methods': ['GET']
                },
                '/health_facilities/search.json': {
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
                    'data': {'health_facilities': []}
                })

            # get health_facilities by that name from aws
            response = {}
            es = Elastic()
            hf = es.get_from_elasticsearch('health-facilities', query)

            if not hf:
                response['message'] = 'No health facility by that name found.'

            track_event(GA_TRACKING_ID,
                        'Health-Facilities', 'search', request.META.get('REMOTE_ADDR'),
                        label=query, value=len(hf))
            response['data'] = {'health_facilities': hf}
            response['status'] = 'success'

            results = jsonify(response, sort_keys=True)
            return results
        except Exception as err:
            return jsonify({
                'status': 'error',
                'message': str(err),
                'data': {'health_facilities': []}
            })
