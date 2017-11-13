import requests
import logging
from bs4 import BeautifulSoup


NURSING_COUNCIL_URL = 'http://nckenya.com/services/search.php?p=1&s={}'
NURSES_FIELDS = ['name', 'licence_no', 'valid_till']

log = logging.getLogger(__name__)

def search(query):
    results = get_nurses_from_nc_registry(query)
    return results


def get_nurses_from_nc_registry(query):
    '''
    Get nurses from the nursing council of Kenya registry
    '''
    url = NURSING_COUNCIL_URL.format(query)
    nurses = {'hits': [], 'total': 0}
    try:
        response = requests.get(url)
        if 'No results' in response.content:
            return nurses

        # make soup for parsing out of response and get the table
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'zebra'}).find('tbody')
        rows = table.find_all("tr")

        # parse table for the nurses data
        for row in rows:
            # only the columns we want
            columns = row.find_all('td')[:len(NURSES_FIELDS)]
            columns = [text.text.strip() for text in columns]

            entry = dict(zip(NURSES_FIELDS, columns))
            nurses['hits'].append(entry)

        nurses['total'] = len(nurses['hits'])

        return nurses
    except Exception as err:
        log.error("Error getting nurses from the nursing council url \n" + str(err))
