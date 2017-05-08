import boto3
from flask import Blueprint, request, jsonify, current_app

from healthtools_ke_api.analytics import track_event
from healthtools_ke_api.settings import AWS_CONFIGS


clinical_officers_api = Blueprint('clinical_officers_api', __name__)
COS_CLOUDSEARCH_ENDPOINT = "http://doc-cfa-healthtools-ke-cos-nhxtw3w5goufkzram4er7sciz4.eu-west-1.cloudsearch.amazonaws.com/"
cloudsearch_client = boto3.client("cloudsearchdomain",
                                  endpoint_url=COS_CLOUDSEARCH_ENDPOINT,
                                  **AWS_CONFIGS)


@clinical_officers_api.route('/', methods=['GET'])
def index():
    '''
    Landing endpoint
    '''
    msg = {
        "name": "API to Kenyan Clinical Officers registry",
        "authentication": [],
        "endpoints": {
            "/": {"methods": ["GET"]},
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
        clinical_officers = get_clinical_officers_from_cloudsearch(query)

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


def get_clinical_officers_from_cloudsearch(query):
    '''
    Get clinical officers from AWS cloudsearch
    '''
    results = cloudsearch_client.search(query=query, size=10000)
    return results["hits"]["hit"]
