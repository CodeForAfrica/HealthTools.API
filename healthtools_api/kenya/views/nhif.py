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
            'name': 'API to Kenyan NHIF registry',
            'authentication': [],
            'endpoints': {
                '/': {
                    'methods': ['GET']
                },
                '/outpatient-cs/search.json': {
                    'name': 'Endpoint for the NHIF accredited outpatient facilities available to civil servants',
                    'methods': ['GET'],
                    'args': {
                        'q': {'required': True}
                    }
                },
                '/outpatient/search.json': {
                    'name': 'Endpoint for the NHIF accredited outpatient facilities available to all kenyans',
                    'methods': ['GET'],
                    'args': {
                        'q': {'required': True}
                    }
                },
                '/inpatient/search.json': {
                    'name': 'Endpoint for the NHIF accredited inpatient facilities available to all kenyans',
                    'methods': ['GET'],
                    'args': {
                        'q': {'required': True}
                    }
                },
            }
        }
        return jsonify(msg, sort_keys=True)


def search_outpatient_cs(request):
    if request.method == 'GET':
        try:
            query = request.GET.get('q')
            if not query or len(query) < 1:
                return jsonify({
                    'error': 'A query is required.',
                    'results': '',
                    'data': {'outpatient_civil_service': []}
                })

            # get facilities by that name from aws
            response = {}
            es = Elastic()
            facility = es.get_from_elasticsearch('nhif-outpatient-cs', query)

            if not facility:
                response['message'] = 'No facility by that name found.'

            track_event(GA_TRACKING_ID,
                        'Outpatient-CS', 'search', request.META.get('REMOTE_ADDR'),
                        label=query, value=len(facility))
            response['data'] = {'outpatient_civil_service': facility}
            response['status'] = 'success'

            results = jsonify(response, sort_keys=True)
            return results
        except Exception as err:
            return jsonify({
                'status': 'error',
                'message': str(err),
                'data': {'outpatient_civil_service': []}
            })


def search_outpatient(request):
    if request.method == 'GET':
        try:
            query = request.GET.get('q')
            if not query or len(query) < 1:
                return jsonify({
                    'error': 'A query is required.',
                    'results': '',
                    'data': {'outpatient': []}
                })

            # get facilities by that name from aws
            response = {}
            es = Elastic()
            facility = es.get_from_elasticsearch('nhif-outpatient', query)

            if not facility:
                response['message'] = 'No facility by that name found.'

            track_event(GA_TRACKING_ID,
                        'Outpatient', 'search', request.META.get('REMOTE_ADDR'),
                        label=query, value=len(facility))
            response['data'] = {'outpatient': facility}
            response['status'] = 'success'

            results = jsonify(response, sort_keys=True)
            return results
        except Exception as err:
            return jsonify({
                'status': 'error',
                'message': str(err),
                'data': {'outpatient': []}
            })


def search_inpatient(request):
    if request.method == 'GET':
        try:
            query = request.GET.get('q')
            if not query or len(query) < 1:
                return jsonify({
                    'error': 'A query is required.',
                    'results': '',
                    'data': {'inpatient': []}
                })

            # get facilities by that name from aws
            response = {}
            es = Elastic()
            facility = es.get_from_elasticsearch('nhif-inpatient', query)

            if not facility:
                response['message'] = 'No facility by that name found.'

            track_event(GA_TRACKING_ID,
                        'Inpatient', 'search', request.META.get('REMOTE_ADDR'),
                        label=query, value=len(facility))
            response['data'] = {'inpatient': facility}
            response['status'] = 'success'

            results = jsonify(response, sort_keys=True)
            return results
        except Exception as err:
            return jsonify({
                'status': 'error',
                'message': str(err),
                'data': {'inpatient': []}
            })