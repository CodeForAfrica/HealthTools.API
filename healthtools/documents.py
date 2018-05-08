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
    'health-facilities': {
        'search_type': 'elastic',
        'keywords': ['hf', 'hospital', 'dispensary', 'clinic', 'hospitali',
                     'sanatorium', 'health centre'],
        'sms_field': 'name'
    },
    'nhif-inpatient': {
        'search_type': 'elastic',
        'keywords': ['inpatient', 'nhif-inpatient', 'nhif inpatient'
                     'bima-inpatient', 'bima inpatient', 
                     'inpatient insurance', 'inpatient insurance fund', 
                     'inpatient health insurance', 'inpatient hospital fund'],
        'sms_field': 'name'
    },
    'nhif-outpatient': {
        'search_type': 'elastic',
        'keywords': ['outpatient', 'nhif-outpatient', 'nhif outpatient'
                     'outpatient insurance', 'bima-outpatient',
                     'bima outpatient', 'outpatient insurance fund',
                     'outpatient health insurance', 'outpatient hospital fund'],
        'sms_field': 'name'
    },
    'nhif-outpatient-cs': {
        'search_type': 'elastic',
        'keywords': ['outpatient-cs', 'nhif-outpatient-cs', 'nhif outpatient cs',  
                     'outpatient-cs insurance', 'outpatient cs insurance', 
                     'outpatient-cs insurance fund','outpatient cs insurance fund', 
                     'outpatient-cs health insurance', 'outpatient cs health insurance',
                     'outpatient cs hospital fund', 'outpatient-cs hospital fund', 
                     'outpatient cs bima', 'outpatient cs-bima', 'outpatient cs insurance', 
                     'outpatient-cs insurance', 'outpatient-cs insurance fund', 
                     'outpatient cs insurance fund', 'outpatient cs health insurance',  
                     'outpatient-cs health insurance', 'outpatient-cs hospital fund', 
                     'outpatient cs hospital fund'
                     ],
        'sms_field': 'name'
    },


}

def get_docs():
    return DOCUMENTS

def doc_exists(doc_type):
    for doc in DOCUMENTS:
        if doc == doc_type:
            return True
    return False
