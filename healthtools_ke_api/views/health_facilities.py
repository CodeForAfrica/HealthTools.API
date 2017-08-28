from flask import Blueprint, request, jsonify, make_response, json, current_app
from bs4 import BeautifulSoup
from elastic_search import Elastic

from healthtools_ke_api.analytics import track_event

import requests

health_facilities_api = Blueprint('health_facilities_api', __name__)

@health_facilities_api.route('/', methods=['GET'])
def index():
    '''
    Landing endpoint
    '''
    msg = {
        "name": "API to the Health Facilities registry",
        "authentication": [],
        "endpoints": {
            "/": {"methods": ["GET"]},
            "/health_facilities/search.json": {
                "methods": ["GET"],
                "args": {
                    "q": {"required": True}
                }
            },
        }
    }
    return jsonify(msg)

@health_facilities_api.route('/search.json', methods=['GET'])
def search():
    try:
        query = request.args.get('q')
        if not query or len(query) < 1:
            return jsonify({
                "error": "A query is required.",
                "results": "",
                "data": {"health_facilities": []}
            })

        response = {}
        es = Elastic()
        health_facilities = es.get_from_elasticsearch('health-facilities', query)

        if not health_facilities:
                response["message"] = "No health facility by that name found."

        track_event(current_app.config.get('GA_TRACKING_ID'), 'Health-Facilities', 'search',
                        request.remote_addr, label=query, value=len(health_facilities))

        response["data"] = {"health facility": health_facilities}
        response["status"] = "success"

        results = jsonify(response)
        return results

    except Exception as err:
        return jsonify({
            "status": "error",
            "message": str(err),
            "data": {"health_facilities": []}
        })
