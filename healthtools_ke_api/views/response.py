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
        "clinical-officers": ['CO', 'clinical officer', 'clinic officer', 'clinical', 'clinical oficer'],
        "NHIF": ['nhif', 'bima', 'insurance', 'insurance fund', 'health insurance', 'hospital fund'],
        "HF": ['hf', 'hospital', 'dispensary', 'clinic', 'hospitali', 'sanatorium', 'health centre']
        }


class BuildQuery(object):
    def __init__(self):
        self.SMS_RESULT_COUNT = 4  # Number of results to be send via sms
        
    # def find_keyword_in_query(self, query, keywords):
    #     regex = re.compile(r'\b(?:%s)\b' % '|'.join(keywords), re.IGNORECASE)
    #     return re.search(regex, query)

    def clean_query(query):
        query = query.lower().split(" ")
        return query

    def find_keyword(query):
        name = clean_query(query)
        quotes = "'"
        for key, value in KEYWORDS.items():
            for x in name:
                if x in value:
                    return '{}{}{}'.format(quotes,key,quotes)

    def build_query_response(query):
        quest = find_keyword(query)
        if find_keyword(query):
            # quest = self.find_keyword(query)
            if quest is 'nurses':
                nurses = get_nurses_from_nc_registry(quest)
                msg = self.construct_responses(nurses[:self.SMS_RESULT_COUNT])
                self.check_message(msg)
                return [msg]

            elif quest is 'NHIF':
                pass
            else:
                search = es.get_from_elasticsearch(quest, query)
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
            msg_items.append("4. NHIF accredited hospital: NHIF KITALE")
            msg_items.append("5. Health Facility: HF KITALE")
            msg = " ".join(msg_items)
            return [msg, {'error': " ".join(msg_items)}]

    def construct_responses(list):
        if len(list) < 1:
            return "Could not find a {} with that name.".format(list.name)
        count = 1
        msg_items = []
        if list is nurse_list:
            status = " ".join([str(count) + ".", nurse['name'].title() + ",", "Valid to", nurse['valid_till'].title()])
        else:
            for parameters in list:
                parameters = parameters['_source']:
                if '_type' is "health-facilities":
                    status = " ".join([str(count) + ".", hf['name'].title() + " -", hf['keph_level_name'].title()])
                elif '_type' is "doctors":
                    status = " ".join([str(count) + ".", "".join(doc['name'].title()), "-",
                                "".join(doc['reg_no'].title()), "-", "".join(doc['qualifications'].upper())])
                elif '_type' is 'clinical-officers':
                    status = " ".join([str(count) + ".", "".join(co['name'].title()), "-", "".join(co['qualifications'].upper())])
                elif '_type' is 'hospital':
                    status = " ".join([str(count) + ".", hospital.title()])
                    
        msg_items.append(status)
        count = count + 1
        if len(list) > 1:
            msg_items.append(
                "\nFind the full list at http://health.the-star.co.ke")
        # print "\n".join(msg_items)
        return "\n".join(msg_items)

    def parse_elastic_search_results(self, response):
        result_to_send_count = self.SMS_RESULT_COUNT
        data_dict = response.json()
        fields_dict = (data_dict['hits'])
        hits = fields_dict['hit']
        result_list = []
        search_results_count = len(hits)
        print "FOUND {} RESULTS".format(search_results_count)
        for item in hits:
            result = item['fields']
            if len(result_list) < result_to_send_count:
                result_list.append(result)
            else:
                break
        return result_list

    def check_message(self, msg):
        # check the message and if query wasn't understood, post error
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
