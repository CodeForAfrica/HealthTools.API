# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from .jsonify import jsonify
from ..analytics import track_event
from ..elastic import Elastic
from ..settings import GA_TRACKING_ID


def index(request):
    '''Landing Endpoint'''
    if request.method == 'GET':
        msg = {
            'name': 'API to the Kenyan doctors registry',
            'authentication': [],
            'endpoints': {
                '/': {'methods': ['GET']},
                '/doctors/search.json': {
                    'methods': ['GET'],
                    'args': {
                        'q': {'required': True}
                    }
                },
            }
        }
        return jsonify(msg, sort_keys=True)


def search(request):
    '''Search endpoint for doctors'''
    if request.method == 'GET':
        try:
            query = request.GET.get('q')
            if not query or len(query) < 1:
                return jsonify({
                    'error': 'A query is required.',
                    'results': '',
                    'data': {'doctors': []}
                    })

            # get doctors by that name from aws
            response = {}
            es = Elastic()
            doctors = es.get_from_elasticsearch('doctors', query)

            if not doctors:
                response['message'] = 'No doctor by that name found.'

            track_event(GA_TRACKING_ID, 'Doctor', 'search',
                        request.META.get('REMOTE_ADDR'), label=query, value=len(doctors))
            response['data'] = {'doctors': doctors}
            response['status'] = 'success'

            return jsonify(response, sort_keys=True)
        except Exception as err:
            return jsonify({
                'status': 'error',
                'message': str(err),
                'data': {'doctors': []}
                })
