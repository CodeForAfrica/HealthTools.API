from flask import Blueprint, request, jsonify, make_response, json, current_app
from bs4 import BeautifulSoup

from healthtools_ke_api.elastic_search import Elastic
from healthtools_ke_api.analytics import track_event

import requests

nhif_inpatient_api = Blueprint('nhif_inpatient_api', __name__)

@nhif_inpatient_api.route('/', methods=['GET'])
def index():
    '''
    Landing endpoint
    '''
    msg = {
        "name": "API to the NHIF inpatient registry",
        "authentication": [],
        "endpoints": {
            "/": {"methods": ["GET"]},
            "/nhif-inpatient/search.json": {
                "methods": ["GET"],
                "args": {
                    "q": {"required": True}
                }
            },
        }
    }
    return jsonify(msg)

@nhif_inpatient_api.route('/search.json', methods=['GET'])
def search():
    try:
        query = request.args.get('q')
        if not query or len(query) < 1:
            return jsonify({
                "error": "A query is required.",
                "results": "",
                "data": {"nhif_inpatient": []}
            })

        response = {}
        es = Elastic()
        nhif_inpatient = es.get_from_elasticsearch('nhif-inpatient', query)

        if not nhif_inpatient:
                response["message"] = "No NHIF inpatient facility by that name found."

        track_event(current_app.config.get('GA_TRACKING_ID'), 'Nhif-Inpatient', 'search',
                        request.remote_addr, label=query, value=len(nhif_inpatient))

        response["data"] = {"nhif_inpatient": nhif_inpatient}
        response["status"] = "success"

        results = jsonify(response)
        return results

    except Exception as err:
        return jsonify({
            "status": "error",
            "message": str(err),
            "data": {"nhif_inpatient": []}
        })