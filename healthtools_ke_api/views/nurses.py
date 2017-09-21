from bs4 import BeautifulSoup
from flask import Blueprint, request, jsonify, make_response, json, current_app

from healthtools_ke_api.analytics import track_event
from healthtools_ke_api.settings import MEMCACHED_URL

import requests
import memcache

nurses_api = Blueprint('nurses_api', __name__)
cache = memcache.Client([MEMCACHED_URL], debug=True)  # cache server

nurse_fields = ["name", "licence_no", "valid_till"]
NURSING_COUNCIL_URL = "http://nckenya.com/services/search.php?p=1&s={}"


@nurses_api.route('/', methods=['GET'])
def index():
    """
    This function displays all the endpoints available
    in the nurses registry.
    Returns:
    json.  The response ::
        {
            "name": "Nursing Council of Kenya API",
            "authentication": [],
            "endpoints": {
                "/": {"methods": ["GET"]},
                "/nurses/search.json": {
                    "methods": ["GET"],
                    "args": {
                        "q": {"required": True}
                    }
                },
            }
        }
    """

    msg = {
        "name": "Nursing Council of Kenya API",
        "authentication": [],
        "endpoints": {
            "/": {"methods": ["GET"]},
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
    """This function searches through the nursing council of Kenya registry
    based on the search query supplied by user.
    Query string: 
         q (str):  The name of the nurse to lookup.
    Returns (JSON):
       The response can be any of the following ::
          When no query string was supplied: 
          {
            "error": "A query is required.",
            "results": "",
            "data": {"nurses": []}
          }
          When no nurse was found
          {
            "message" = "No nurse by that name found."
          }
          when nurse(s) was found
          {
            "data": {"nurses": <list_of_nurses>},
            "status": "success",
                
          }
          When an error occurs
          {
              "status": "error",
              "message": <error_message>,
              "data": {"nurses": []}
          }
    """

    try:
        query = request.args.get('q')
        if not query or len(query) < 1:
            return jsonify({
                "error": "A query is required.",
                "results": "",
                "data": {"nurses": []}
                })

        # try to get queried result first
        cached_result = cache.get(query.replace(" ", ""))
        if cached_result:
            num_cached_results = len(json.loads(
                cached_result.data)["data"]["nurses"])
            track_event(current_app.config.get('GA_TRACKING_ID'), 'Nurse', 'search',
                        request.remote_addr, label=query, value=num_cached_results)
            response = make_response(cached_result)
            response.headers["X-Retrieved-From-Cache"] = True
            return response

        # get nurses by that name from nursing council site
        response = {}
        nurses = get_nurses_from_nc_registry(query)
        if not nurses:
            response["message"] = "No nurse by that name found."

        # send action to google analytics
        track_event(current_app.config.get('GA_TRACKING_ID'),
                    'Nurse', 'search',
                    request.remote_addr, label=query, value=len(nurses))

        response["data"] = {"nurses": nurses}
        response["status"] = "success"

        results = jsonify(response)
        cache.set(query.replace(" ", ""), results,
                  time=345600)  # expire after 4 days
        return results

    except Exception as err:
        return jsonify({
            "status": "error",
            "message": str(err),
            "data": {"nurses": []}
        })


def get_nurses_from_nc_registry(query):
    '''
    Get nurses from the nursing council of Kenya registry
    '''
    url = NURSING_COUNCIL_URL.format(query)
    response = requests.get(url)
    nurses = []

    if "No results" in response.content:
        return nurses

    # make soup for parsing out of response and get the table
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", {"class": "zebra"}).find("tbody")
    rows = table.find_all("tr")

    # parse table for the nurses data
    for row in rows:
        # only the columns we want
        columns = row.find_all("td")[:len(nurse_fields)]
        columns = [text.text.strip() for text in columns]

        entry = dict(zip(nurse_fields, columns))
        nurses.append(entry)

    return nurses
