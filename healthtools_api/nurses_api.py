from bs4 import BeautifulSoup
from healthtools_api.config import NURSING_COUNCIL_URL
import requests

nurse_fields = ["name", "licence_no", "valid_till"]


def find_nurse(query):
    try:
        url = NURSING_COUNCIL_URL.format(query)
        response = requests.get(url)

        if "No results" in response.content:
            return "No nurse by that name found."

        soup = BeautifulSoup(response.content, "html.parser")
        table = soup.find('table', {"class": "zebra"}).find("tbody")
        rows = table.find_all("tr")

        entries = []

        for row in rows:
            # only the columns we want
            columns = row.find_all("td")[:len(nurse_fields)]
            columns = [text.text.strip() for text in columns]

            entry = dict(zip(nurse_fields, columns))
            entries.append(entry)
        return entries

    except Exception as err:
        print "ERROR: {} ".format(str(err))
