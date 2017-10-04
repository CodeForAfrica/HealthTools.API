from nested_lookup import nested_lookup

DOCUMENTS = {
    'doctors': {
        'search_type': 'elastic',
        'keywords': ['doc', 'daktari', 'doctor', 'oncologist', 'dr'],
        'sms_field': 'name'
    },
    'clinical-officers': {
        'search_type': 'elastic',
        'keywords': ['CO', 'clinical officer', 'clinic officer', 'clinical',
                     'clinical oficer'],
        'sms_field': 'name'
    },
    'nurses': {
        'search_type': 'nurses',
        'keywords': ['nurse', 'no', 'nursing officer', 'mhuguzi', 'muuguzi',
                     'RN', 'Registered Nurse'],
        'sms_field': 'name'
    },
    'nhif' : {
        'doc_name': ['nhif-inpatient', 'nhif-outpatient', 'nhif-outpatient-cs'],
        'search_type': 'elastic',
        'keywords': ['nhif', 'bima', 'insurance', 'insurance fund',
                     'health insurance', 'hospital fund'],
        'sms_field': 'name'
    },
    'health-facilities': {
        'search_type': 'elastic',
        'keywords': ['hf', 'hospital', 'dispensary', 'clinic', 'hospitali',
                     'sanatorium', 'health centre'],
        'sms_field': 'name'
    },


}


def get_docs():
    return DOCUMENTS

def doc_exists(doc_type):
    if doc_type in DOCUMENTS['nhif']['doc_name']:
        return True
    elif nested_lookup(doc_type, DOCUMENTS):
        return True
    else:
        return False
