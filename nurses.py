from bs4 import BeautifulSoup
from config import NURSING_COUNCIL_URL
from flask import Flask, request
from werkzeug.exceptions import HTTPException, default_exceptions
import requests
import json


app = Flask(__name__)

nurse_fields = ["name", "licence_no", "valid_till"]


@app.route('/find_nurse', methods=['GET'])
def find_nurse():
    try:
        query = request.args.get('q')
        if not query or len(query) < 1:
            return json.dumps({
                              "error": "A query is required.",
                              "results": ""
                              })
        url = NURSING_COUNCIL_URL.format(query)
        response = requests.get(url)

        if "No results" in response.content:
            return json.dumps({"results": "No nurse by that name found."})

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
        return json.dumps({"results": entries})

    except Exception as err:
        return json.dumps({
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
    return json.dumps(response), status_code


# change error handler for all http exceptions to return json instead of html
for code in default_exceptions.keys():
    app.errorhandler(code)(handle_error)

if __name__ == "__main__":
    app.run(debug=True)
