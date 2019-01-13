DOCUMENTS = {
    'doctors': {
        'search_type': 'elastic',
        'keywords': ['doc', 'daktari', 'doctor', 'oncologist', 'dr'],
        'sms_field': 'name'
    },
    'clinical-officers': {
        'search_type': 'clinicalofficers',
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
    # Default NHIF response
    'nhif-inpatient': {
        'search_type': 'elastic',
        'keywords': ['nhif', 'inpatient', 'nhif-inpatient', 'nhif inpatient'
                     'nhif in', 'nhif-in', 'nhif-inn', 'nhifin',
                     'bima-inpatient', 'bima inpatient', 
                     'inpatient insurance', 'inpatient insurance fund', 
                     'inpatient health insurance', 'inpatient hospital fund'],
        'sms_field': 'hospital'
    },
    'nhif-outpatient': {
        'search_type': 'elastic',
        'keywords': ['outpatient', 'nhif-outpatient', 'nhif outpatient',
                     'nhif out', 'nhif-out', 'nhif-outt', 'nhifout',
                     'outpatient insurance', 'bima-outpatient',
                     'bima outpatient', 'outpatient insurance fund',
                     'outpatient health insurance', 'outpatient hospital fund'],
        'sms_field': 'hospital'
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
        'sms_field': 'hospital'
    },


}

# Duplicate for robust
DOCUMENTS['doctors-foreign'] = DOCUMENTS['doctors']
DOCUMENTS['nhif'] = DOCUMENTS['nhif-inpatient']

def get_docs():
    return DOCUMENTS

def get_sms_field(doc_type):
    return DOCUMENTS[doc_type]['sms_field']

def doc_exists(doc_type):
    for doc in DOCUMENTS:
        if doc == doc_type:
            return True
    return False
