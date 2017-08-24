import re
import requests
import string

from flask import Blueprint, request, current_app

from healthtools_ke_api.analytics import track_event
from healthtools_ke_api.views.nurses import get_nurses_from_nc_registry
from healthtools_ke_api.elastic_search import Elastic


es = Elastic()


class BuildQuery(object):
    def __init__(self):
        self.SMS_RESULT_COUNT = 4  # Number of results to be send via sms
        self.DOC_KEYWORDS = ['doc', 'daktari', 'doctor', 'oncologist', 'dr']
        self.CO_KEYWORDS = ['CO', 'clinical officer',
                            'clinic officer', 'clinical', 'clinical oficer', ]
        self.NO_KEYWORDS = ['nurse', 'no', 'nursing officer',
                            'mhuguzi', 'muuguzi', 'RN', 'Registered Nurse']
        self.NHIF_KEYWORDS = ['nhif', 'bima', 'insurance',
                              'insurance fund', 'health insurance', 'hospital fund']
        self.HF_KEYWORDS = ['hf', 'hospital', 'dispensary', 'clinic',
                            'hospitali', 'sanatorium', 'health centre']

    def find_keyword_in_query(self, query, keywords):
        regex = re.compile(r'\b(?:%s)\b' % '|'.join(keywords), re.IGNORECASE)
        return re.search(regex, query)

    def build_query_response(self, query):
        query = self.clean_query(query)
        # Start by looking for doctors keywords
        if self.find_keyword_in_query(query, self.DOC_KEYWORDS):
            search_terms = self.find_keyword_in_query(query, self.DOC_KEYWORDS)
            query = query[:search_terms.start()] + query[search_terms.end():]
            print query
            doctors = es.get_from_elasticsearch('doctors', query)
            msg = self.construct_docs_response(doctors[:self.SMS_RESULT_COUNT])
            return [msg]
        # Looking for Nurses keywords
        elif self.find_keyword_in_query(query, self.NO_KEYWORDS):
            search_terms = self.find_keyword_in_query(query, self.NO_KEYWORDS)
            query = query[:search_terms.start()] + query[search_terms.end():]
            nurses = get_nurses_from_nc_registry(query)
            msg = self.construct_nurse_response(nurses[:self.SMS_RESULT_COUNT])
            return [msg]
        # Looking for clinical officers Keywords
        elif self.find_keyword_in_query(query, self.CO_KEYWORDS):
            search_terms = self.find_keyword_in_query(query, self.CO_KEYWORDS)
            query = query[:search_terms.start()] + query[search_terms.end():]
            print query
            clinical_officers = es.get_from_elasticsearch(
                'clinical-officers', query)
            msg = self.construct_co_response(
                clinical_officers[:self.SMS_RESULT_COUNT])
            return [msg]
        # Looking for nhif hospitals
        elif self.find_keyword_in_query(query, self.NHIF_KEYWORDS):
            search_terms = self.find_keyword_in_query(
                query, self.NHIF_KEYWORDS)
            query = query[:search_terms.start()] + query[search_terms.end():]

            if re.search("inpatient", query):
                query = re.sub("\s*inpatient\s*", "",
                               query, flags=re.IGNORECASE)
                doc_type = "nhif-inpatient"
            else:
                query = re.sub("\s*outpatient\s*", "",
                               query, flags=re.IGNORECASE)

                # Default: ES doc_type = nhif-outpatient-cs
                doc_type = ["nhif-outpatient", "nhif-outpatient-cs"]

            nhif_hospitals = es.get_from_elasticsearch(
                doc_type, query)

            msg = self.construct_nhif_response(nhif_hospitals)
            print msg
            return [msg]
        # Looking for health facilities
        elif self.find_keyword_in_query(query, self.HF_KEYWORDS):
            search_terms = self.find_keyword_in_query(query, self.HF_KEYWORDS)
            query = query[:search_terms.start()] + query[search_terms.end():]
            health_facilities = es.get_from_elasticsearch(
                'health-facilities', query)
            msg = self.construct_hf_response(
                health_facilities[:self.SMS_RESULT_COUNT])
            print msg
            return [msg]
        # If we miss the keywords then reply with the preferred query formats
        else:
            msg_items = []
            msg_items.append("We could not understand your query. Try these:")
            msg_items.append("1. Doctors: DR. SAMUEL AMAI")
            msg_items.append("2. Clinical Officers: CO SAMUEL AMAI")
            msg_items.append("3. Nurses: NURSE SAMUEL AMAI")
            msg_items.append("4. NHIF accredited hospital: NHIF KITALE")
            msg_items.append("5. Health Facility: HF KITALE")
            msg = " ".join(msg_items)
            print msg
            return [msg, {'error': " ".join(msg_items)}]

    def construct_co_response(self, co_list):
        # Just incase we found ourselves here with an empty list
        if len(co_list) < 1:
            return "Could not find a clinical officer with that name."
        count = 1
        msg_items = []
        for co in co_list:
            # co = co["fields"]
            co = co["_source"]
            status = " ".join(
                [str(count) + ".", "".join(co['name'].title()), "-", "".join(co['qualifications'].upper())])
            msg_items.append(status)
            count = count + 1
        if len(co_list) > 1:
            msg_items.append(
                "\nFind the full list at http://health.the-star.co.ke")
        print "\n".join(msg_items)
        return "\n".join(msg_items)

    def construct_docs_response(self, docs_list):
        # Just incase we found ourselves here with an empty list
        if len(docs_list) < 1:
            return "Could not find a doctor with that name"
        count = 1
        msg_items = []

        for doc in docs_list:
            doc = doc["_source"]
            status = " ".join([str(count) + ".", "".join(doc['name'].title()), "-",
                               "".join(doc['reg_no'].title()), "-", "".join(doc['qualifications'].upper())])

            msg_items.append(status)
            count = count + 1
        if len(docs_list) > 1:
            msg_items.append(
                "\nFind the full list at http://health.the-star.co.ke")

        return "\n".join(msg_items)

    def construct_nurse_response(self, nurse_list):
        # Just incase we found ourselves here with an empty list
        if len(nurse_list) < 1:
            return "Could not find a nurse with that name"
        count = 1
        msg_items = []
        for nurse in nurse_list:
            status = " ".join([str(count) + ".", nurse['name'].title() +
                               ",", "Valid to", nurse['valid_till'].title()])
            msg_items.append(status)
            count = count + 1
        if len(nurse_list) > 1:
            msg_items.append(
                "\nFind the full list at http://health.the-star.co.ke")

        return "\n".join(msg_items)

    def construct_nhif_response(self, nhif_list):
        # Just incase we found ourselves here with an empty list
        if len(nhif_list) < 1:
            return "We could not find an NHIF accredited hospital with the name or in the location you provided."
        count = 1
        msg_items = []
        nhif_hospitals = []

        for nhif in nhif_list:
            nhif = nhif['_source']
            hospital = nhif['hospital']
            nhif_hospitals.append(hospital)

        nhif_hospitals = list(set(nhif_hospitals))

        for hospital in nhif_hospitals:
            status = " ".join([str(count) + ".", hospital.title()])
            msg_items.append(status)
            count = count + 1

        if len(nhif_list) > 1:
            msg_items.append(
                "\nFind the full list at http://health.the-star.co.ke")

        return "\n".join(msg_items)

    def construct_hf_response(self, hf_list):
        # Just incase we found ourselves here with an empty list
        if len(hf_list) < 1:
            return "We could not find a health facility with the name or in the location you provided."
        count = 1
        msg_items = []
        for hf in hf_list:
            hf = hf['_source']
            status = " ".join([str(count) + ".", hf['name'].title() +
                               " -", hf['keph_level_name'].title()])
            msg_items.append(status)
            count = count + 1
        if len(hf_list) > 1:
            msg_items.append(
                "\nFind the full list at http://health.the-star.co.ke")

        return "\n".join(msg_items)

    def clean_query(self, query):
        query = query.lower().strip().replace(".", "")
        return query

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
