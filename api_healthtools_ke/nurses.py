from bs4 import BeautifulSoup
from api_healthtools_ke.config import MEMCACHED_URL, GA_TRACKING_ID
from api_healthtools_ke.analytics import track_event
from flask import Flask, Blueprint, request, jsonify, make_response, json
import requests
import memcache


nurses_api = Blueprint('nurses_api', __name__)
cache = memcache.Client([(MEMCACHED_URL)], debug=True)  # cache server

nurse_fields = ["name", "licence_no", "valid_till"]
NURSING_COUNCIL_URL = "http://nckenya.com/services/search.php?p=1&s={}"


@nurses_api.route('/', methods=['GET'])
def home():
    '''
    Landing endpoint
    '''
    msg = {
        "name": "Nursing Council of Kenya API",
        "authentication": [],
        "endpoints": {
            "/": {"methods": ["GET"]},
            "/nurses": {
                "methods": ["GET"],
                "args": {
                    "q": {"required": True}
                }
            },
        }
    }
    return jsonify(msg)


@nurses_api.route('/search.json', methods=['GET'])
def find_nurse():
    try:
        query = request.args.get('q')
        if not query or len(query) < 1:
            return jsonify({
                "error": "A query is required.",
                "results": ""
            })

        cached_result = cache.get(query)
        if cached_result:
            num_cached_results = len(json.loads(
                cached_result.data)["data"]["nurses"])
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

        # send action to google analytics
        track_event(GA_TRACKING_ID, 'Nurse', 'search',
                    request.remote_addr, label=query, value=len(entries))
        results = jsonify({"status": "success", "data": {"nurses": entries}})
        cache.set(query, results, time=345600)  # expire after 4 days
        return results

    except Exception as err:
        return jsonify({
            "status": "error",
            "message": str(err),
        })
