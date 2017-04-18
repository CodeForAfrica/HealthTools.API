import requests

from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify, make_response, json
from werkzeug.exceptions import HTTPException, default_exceptions
from memcache import Client

from healthtools_ke_api.config import *
from healthtools_ke_api.analytics import track_event

nurses_api = Blueprint('nurses_api', __name__)
nurse_fields = ["name", "licence_no", "valid_till"]
cache = Client([(MEMCACHED_URL)], debug=True)

NURSING_COUNCIL_URL = 'http://nckenya.com/services/search.php?p=1&s={}'


@nurses_api.route('/', methods=['GET'])
def index():
    '''
    Landing endpoint
    '''
    msg = {
        "name": "Nursing Council of Kenya API",
        "authentication": [],
        "endpoints": {
            "/nurses": {"methods": ["GET"]},
            "/nurses/search.json": {
                "methods": ["GET"],
                "args": {
                    "q": {"required": True}
                }
            },
        }
    }
    return jsonify(msg)


@nurses_api.route('/search.json', methods=['GET'])
def search():
    try:
        query = request.args.get('q')
        if not query or len(query) < 1:
            return jsonify({
                "error": "A query is required.",
                "results": ""
            })

        cached_result = cache.get(query)
        if cached_result:
            num_cached_results = len(json.loads(cached_result.data)["data"]["nurses"])
            track_event(GA_TRACKING_ID, 'Nurse', 'search',
                        request.remote_addr, label=query, value=num_cached_results)
            response = make_response(cached_result)
            response.headers["X-Retrieved-From-Cache"] = True
            return response

        url = NURSING_COUNCIL_URL.format(query)
        response = requests.get(url)

        if "No results" in response.content:
            track_event(GA_TRACKING_ID, 'Nurse', 'search',
                        request.remote_addr, label=query, value=0)
            return jsonify({
                           "status": "success",
                           "message": "No nurse by that name found."
                           })

        # make soup for parsing out of response and get the table
        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table', {"class": "zebra"}).find("tbody")
        rows = table.find_all("tr")

        entries = []

        # parse table for the nurses data
        for row in rows:
            # only the columns we want
            columns = row.find_all("td")[:len(nurse_fields)]
            columns = [text.text.strip() for text in columns]

            entry = dict(zip(nurse_fields, columns))
            entries.append(entry)

        # Cache the results
        cache.set(query, results, time=345600)  # expire after 4 days

        # Send action to google analytics
        track_event(
                GA_TRACKING_ID, 'Nurse', 'search', request.remote_addr,
                label=query, value=len(entries))

        results = jsonify({"status": "success", "data": {"nurses": entries}})

        return results

    except Exception as err:
        return jsonify({
            "status": "error",
            "message": str(err),
        })


def handle_error(error):
    '''Generic error handlers for all http exceptions'''
    response = {}
    status_code = 500
    if isinstance(error, HTTPException):
        status_code = error.code
    response["status_code"] = status_code
    response["error"] = str(error)
    response['description'] = error.description
    return jsonify(response), status_code


# change error handler for all http exceptions to return json instead of html
for code in default_exceptions.keys():
    nurses_api.errorhandler(code)(handle_error)
