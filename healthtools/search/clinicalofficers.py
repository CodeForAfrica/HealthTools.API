import requests
import logging
from bs4 import BeautifulSoup


COC_REGISTER_URL = 'https://portal.clinicalofficerscouncil.org/practice/ajax/public'
TABLE_FIELDS = ['name', 'licence_no', 'valid_till']

log = logging.getLogger(__name__)

def search(query):
    results = get_clinical_officers(query)
    return results


def get_clinical_officers(query):
    '''
    Get COs from the COC Register 
    '''
    clinicalofficers = {'hits': [], 'total': 0}
    try:
        response = requests.post(COC_REGISTER_URL, data = {'search_register':'1', 'search_text': query})
        if 'No results' in response.content:
            return clinicalofficers

        # make soup for parsing out of response and get the table
        soup = BeautifulSoup(response.content, 'html.parser')
        table = soup.find('table', {'class': 'datatables'}).find('tbody')
        rows = table.find_all("tr")

        # parse table for the clinicalofficers data
        for row in rows:
            # only the columns we want
            columns = row.find_all('td')[:len(TABLE_FIELDS)]
            columns = [text.text.strip() for text in columns]

            entry = dict(zip(TABLE_FIELDS, columns))
            clinicalofficers['hits'].append(entry)

        clinicalofficers['total'] = len(clinicalofficers['hits'])

        return clinicalofficers
    except Exception as err:
        log.error("Error getting clinicalofficers from the register \n" + str(err))
