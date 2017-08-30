from flask import Blueprint, request, jsonify, current_app

from healthtools_ke_api.elastic_search import Elastic
from healthtools_ke_api.analytics import track_event

clinical_officers_api = Blueprint('clinical_officers_api', __name__)


@clinical_officers_api.route('/', methods=['GET'])
def index():
    '''
    Landing endpoint
    '''
    msg = {
        "name": "API to Kenyan Clinical Officers registry",
        "authentication": [],
        "endpoints": {
            "/": {
                "methods": ["GET"]
            },
            "/clinical-officers/search.json": {
                "methods": ["GET"],
                "args": {
                    "q": {"required": True}
                }
            },
        }
    }
    return jsonify(msg)


@clinical_officers_api.route('/search.json', methods=['GET'])
def search():
    try:
        query = request.args.get('q')
        if not query or len(query) < 1:
            return jsonify({
                "error": "A query is required.",
                "results": "",
                "data": {"clinical_officers": []}
            })

        # get clinical_officers by that name from aws
        response = {}
        es = Elastic()
        clinical_officers = es.get_from_elasticsearch('clinical-officers', query)

        if not clinical_officers:
            response["message"] = "No clinical officer by that name found."

        track_event(current_app.config.get('GA_TRACKING_ID'),
                    'Clinical-Officers', 'search', request.remote_addr,
                    label=query, value=len(clinical_officers))
        response["data"] = {"clinical_officers": clinical_officers}
        response["status"] = "success"

        results = jsonify(response)
        return results
    except Exception as err:
        return jsonify({
            "status": "error",
            "message": str(err),
            "data": {"clinical_officers": []}
        })
