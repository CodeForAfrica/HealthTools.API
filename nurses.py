from bs4 import BeautifulSoup
from config import NURSING_COUNCIL_URL, MEMCACHED_URL, GA_TRACKING_ID
from flask import Flask, request, jsonify, make_response, json
from werkzeug.exceptions import HTTPException, default_exceptions
import requests
import memcache


app = Flask(__name__)
cache = memcache.Client([(MEMCACHED_URL)], debug=True)  # cache server

nurse_fields = ["name", "licence_no", "valid_till"]


@app.route('/', methods=['GET'])
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


@app.route('/nurses', methods=['GET'])
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


def track_event(tracking_id, category, action, cid, label=None, value=0):
    '''
    Posts Tracking in info to Google Analytics using measurement protocol.
    Args:
        tracking_id: The tracking ID of the Google Analytics account in which these data is associated with.
        category: The name assigned to the group of similar events to track.
        action: The Specific action being tracked.
        cid: Anonymous Client Identifier. Ideally, this should be a UUID that is associated with particular user, device
        label: Label of the event.
        value: Value of event in this case number of results obtained
    Returns:
        No return value # If the request fails, it will raise a RequestException. .
    '''
    data = {
        'v': '1',
        'tid': tracking_id,
        'cid': cid,
        't': 'event',
        'ec': category,
        'ea': action,
        'el': label,
        'ev': value,
    }
    response = requests.post(
        'http://www.google-analytics.com/collect', data=data)
    response.raise_for_status()


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
    app.errorhandler(code)(handle_error)

if __name__ == "__main__":
    app.run(debug=True, port=5555)
