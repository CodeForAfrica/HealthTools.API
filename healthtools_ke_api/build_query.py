import getpass
import json
import requests
import re

from datetime import datetime
from flask import Blueprint, request, current_app

from healthtools_ke_api.analytics import track_event
from healthtools_ke_api.views.nurses import get_nurses_from_nc_registry
from healthtools_ke_api.elastic_search import Elastic

es = Elastic()

KEYWORDS = {
        "doctors": ['doc', 'daktari', 'doctor', 'oncologist', 'dr'],
        "nurses": ['nurse', 'no', 'nursing officer', 'mhuguzi', 'muuguzi', 'RN', 'Registered Nurse'],
        "clinical-officers": ['co', 'clinical officer', 'clinic officer', 'clinical', 'clinical oficer'],
        "NHIF": ['nhif', 'bima', 'insurance', 'insurance fund', 'health insurance', 'hospital fund'],
        "health-facilities": ['hf', 'hospital', 'dispensary', 'clinic', 'hospitali', 'sanatorium', 'health centre']
        }

class BuildQuery(object):
    def __init__(self):
        self.SMS_RESULT_COUNT = 4  # Number of results to be send via sms
        
    def clean_query(self, query): 
        ''' removes period from the query, changes the query into a lowercased list '''
        query = query.replace(".","")
        query = query.lower().split(" ")
        return query

    def find_keyword_and_search_term(self, query):
        '''this function distinguishes the keyword from the name to be searched. '''
        keyword= []
        names = self.clean_query(query)
        for key, value in KEYWORDS.items():
            for name in names:
                if name in value:
                    keyword.append(key) #
                    names.remove(name) 
                    return (" ".join(names)), (" ".join(keyword))


    def build_query_response(self, query):
        ''' Search elastic search using the specified keyword and search parameter and returns a list'''
        
        query = self.find_keyword_and_search_term(query)
        q = (" ".join((query[:1])))
        quest = (" ".join((query[1:])))
        if quest:
            if quest == 'nurses':
                nurses = get_nurses_from_nc_registry(q)
                msg = self.construct_nurses_responses(nurses[:self.SMS_RESULT_COUNT])
                self.check_message(msg)
                return [msg]

            elif quest == 'NHIF':
                if re.search("inpatient", query):
                    q = re.sub("\s*inpatient\s*", "",
                               q, flags=re.IGNORECASE)
                    doc_type = "nhif-inpatient"
                else:
                    q = re.sub("\s*outpatient\s*", "",
                               q, flags=re.IGNORECASE)

                    # Default: ES doc_type = nhif-outpatient-cs
                    doc_type = ["nhif-outpatient", "nhif-outpatient-cs"]

                nhif_hospitals = es.get_from_elasticsearch(doc_type, q)
                msg = self.construct_responses(nhif_hospitals[:self.SMS_RESULT_COUNT])
                self.check_message(msg)
                return [msg]

            else:
                search = es.get_from_elasticsearch(quest, q)
                msg = self.construct_responses(search[:self.SMS_RESULT_COUNT])
                self.check_message(msg)
                return [msg]

        # If we miss the keywords then reply with the preferred query formats
        else:
            self.print_error(query)
            msg_items = list()
            msg_items.append("We could not understand your query. Try these:")
            msg_items.append("1. Doctors: DR. SAMUEL AMAI")
            msg_items.append("2. Clinical Officers: CO SAMUEL AMAI")
            msg_items.append("3. Nurses: NURSE SAMUEL AMAI")
            msg_items.append("4. NHIF accredited hospital: NHIF KITALE or NHIF INPATIENT KITALE")
            msg_items.append("5. Health Facility: HF KITALE")
            msg = " ".join(msg_items)
            return [msg, {'error': " ".join(msg_items)}]
    
    def construct_responses(self, docs_list):
        ''' creates responses for NHIF, doctors, health facilitites and clinical officers '''

        hospitals = ['nhif-outpatient-cs', 'nhif-outpatient','nhif-inpatient' ]

        if len(docs_list) < 1:
            return "Could not find search result with that name."
            
        count = 1
        msg_items = []
        if filter(lambda docs_list: docs_list['_type'] == 'doctors', docs_list):
            for doc in docs_list:
                doc = doc['_source']
                status = " ".join([str(count) + ".", "".join(doc['name'].title()), "-",
                        "".join(doc['reg_no'].title()), "-", "".join(doc['qualifications'].upper())])
        elif filter(lambda docs_list: docs_list['_type'] == 'clinical-officers', docs_list):
            for co in docs_list:
                co = co['_source']
                status = " ".join([str(count) + ".", "".join(co['name'].title()), "-", "".join(co['qualifications'].upper())])
        elif filter(lambda docs_list: docs_list['_type'] in hospitals, docs_list):
                for cs in docs_list:
                    cs = cs['_source']
                    status = " ".join([str(count) + ".", cs['hospital'].title()])
        elif filter(lambda docs_list: docs_list['_type'] == 'health-facilities', docs_list):
            for hf in docs_list:
                hf = hf['_source']
                status = " ".join([str(count) + ".", hf['name'].title() + " -", hf['keph_level_name'].title()])
        else:
            return "fail"
        
        msg_items.append(status)
        count = count + 1
        if len(docs_list) > 1:
            msg_items.append(
                "\nFind the full list at http://health.the-star.co.ke")
        return "\n".join(msg_items)

    def construct_nurses_responses(self, docs_list):
        '''
         creates response for nurses
        '''
        if [len(docs_list)] < 1:
            return "Could not find a Nurse with that name."
        count = 1
        msg_items = []
        for nurse in docs_list:
                status = " ".join([str(count) + ".", nurse['name'].title() + ",", "Valid to", nurse['valid_till'].title()])

        msg_items.append(status)
        count = count + 1
        if len(docs_list) > 1:
            msg_items.append(
                "\nFind the full list at http://health.the-star.co.ke")
        return "\n".join(msg_items)

    def check_message(self, msg):
        '''
        check the message and if query wasn't understood, post error
        '''
        if 'could not find' in msg:
            self.print_error(msg)

    def print_error(self, message):
        """		
        print error messages in the terminal
        if slack webhook is set up, post the errors to slack
        """
        print("[{0}] - ".format(datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")) + message)
        response = None
        if SLACK["url"]:
            response = requests.post(
                SLACK["url"],
                data=json.dumps({
                    "attachments": [{
                        "author_name": "HealthTools API",
                        "color": "warning",
                        "pretext": "[SMS] Could not find a result for this SMS.",
                        "fields": [{
                            "title": "Message",
                            "value": message,
                            "short": False
                        }]
                    }]
                }),
                headers={"Content-Type": "application/json"})
        return response
