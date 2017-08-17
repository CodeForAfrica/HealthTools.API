from flask import Blueprint, request, jsonify, current_app

from healthtools_ke_api.analytics import track_event
from search import Elastic

doctors_api = Blueprint('doctors_api', __name__)


@doctors_api.route('/', methods=['GET'])
def index():
    '''
    Landing endpoint
    '''
    msg = {
        "name": "API to the Kenyan doctors registry",
        "authentication": [],
        "endpoints": {
            "/": {"methods": ["GET"]},
            "/doctors/search.json": {
                "methods": ["GET"],
                "args": {
                    "q": {"required": True}
                }
            },
        }
    }
    return jsonify(msg)


@doctors_api.route('/search.json', methods=['GET'])
def search():
    try:
        query = request.args.get('q')
        if not query or len(query) < 1:
            return jsonify({
                "error": "A query is required.",
                "results": "",
                "data": {"doctors": []}
            })

        # get doctors by that name from aws
        response = {}
        es = Elastic()
        doctors = es.get_from_elasticsearch('doctors', query)

        if not doctors:
            response["message"] = "No doctor by that name found."

        track_event(current_app.config.get('GA_TRACKING_ID'), 'Doctor', 'search',
                    request.remote_addr, label=query, value=len(doctors))
        response["data"] = {"doctors": doctors}
        response["status"] = "success"

        results = jsonify(response)
        return results
    except Exception as err:
        return jsonify({
            "status": "error",
            "message": str(err),
            "data": {"doctors": []}
        })
