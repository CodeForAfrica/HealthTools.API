import boto3
from flask import Blueprint, request, jsonify, current_app

from healthtools_ke_api.analytics import track_event
from healthtools_ke_api.settings import AWS_CONFIGS


doctors_api = Blueprint('doctors_api', __name__)
DOCTORS_CLOUDSEARCH_ENDPOINT = "http://doc-cfa-healthtools-ke-doctors-m34xee6byjmzcgzmovevkjpffy.eu-west-1.cloudsearch.amazonaws.com/"
cloudsearch_client = boto3.client("cloudsearchdomain",
                                  endpoint_url=DOCTORS_CLOUDSEARCH_ENDPOINT,
                                  **AWS_CONFIGS)


@doctors_api.route('/', methods=['GET'])
def index():
    '''
    Landing endpoint
    '''
    msg = {
        "name": "API to doctors registry on AWS Cloudsearch",
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
        doctors = get_doctors_from_cloudsearch(query)

        if not doctors:
            response["message"] = "No doctor by that name found."

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


def get_doctors_from_cloudsearch(query):
    '''
    Get doctors from AWS cloudsearch
    '''
    results = cloudsearch_client.search(query=query)
    return results["hits"]["hit"]
