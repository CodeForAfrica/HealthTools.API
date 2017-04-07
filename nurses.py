from bs4 import BeautifulSoup
from config import NURSING_COUNCIL_URL
import requests
import json

nurse_fields = ["name", "licence_no", "valid_till"]


def find_nurse(event, context):
    try:
        query = event["query"]
        if len(query) < 1:
            return json.dumps({
                              "error": "Query cannot be empty.",
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
