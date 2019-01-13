import requests
import logging
from bs4 import BeautifulSoup


FETCH_URL = 'https://osp.nckenya.com/ajax/public'
TABLE_FIELDS = ['name', 'licence_no', 'valid_till']

log = logging.getLogger(__name__)

def search(query):
    results = get_people(query)
    return results


def get_people(query):
    '''
    Get people from the Register 
    '''
    people = {'hits': [], 'total': 0}
    try:
        response = requests.post(FETCH_URL, data = {'search_register':'1', 'search_text': query})
        if 'No results' in response.content:
            return people

        # make soup for parsing out of response and get the table
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'datatables'}).find('tbody')
        rows = table.find_all("tr")

        # parse table for the people data
        for row in rows:
            # only the columns we want
            columns = row.find_all('td')[:len(TABLE_FIELDS)]
            columns = [text.text.strip() for text in columns]

            entry = dict(zip(TABLE_FIELDS, columns))
            people['hits'].append(entry)

        people['total'] = len(people['hits'])

        return people
    except Exception as err:
        log.error("Error getting people from the register \n" + str(err))
