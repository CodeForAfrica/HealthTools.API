from bs4 import BeautifulSoup
from config import NURSING_COUNCIL_URL, MEMCACHED_URL
from flask import Flask, request, jsonify, make_response
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
            "/find_nurse": {
                "methods": ["GET"],
                "args": {
                    "q": {"required": True}
                }
            },
        }
    }
    return jsonify(msg)


@app.route('/find_nurse', methods=['GET'])
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
            response = make_response(cached_result)
            response.headers["X-Retrieved-From-Cache"] = True
            return response

        url = NURSING_COUNCIL_URL.format(query)
        response = requests.get(url)

        if "No results" in response.content:
            return jsonify({"results": "No nurse by that name found."})

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
        results = jsonify({"results": entries})
        cache.set(query, results, time=345600)  # expire after 4 days
        return results

    except Exception as err:
        return jsonify({
            "error": str(err),
            "results": ""
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
    app.errorhandler(code)(handle_error)

if __name__ == "__main__":
    app.run(debug=True, port=5555)
