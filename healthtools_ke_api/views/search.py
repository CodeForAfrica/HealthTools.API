from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from healthtools_ke_api.settings import AWS, ES
from json_serializer import JSONSerializerPython2
import re


class Elastic(object):
    """
    Common class for elastic search client and methods
    """
    def __init__(self):
        # client host for aws elastic search service
        if "aws" in ES["host"]:
            # set up authentication credentials
            awsauth = AWS4Auth(AWS["access_key"], AWS["secret_key"], AWS["region"], 'es')
            self.es_client = Elasticsearch(
                hosts=ES["host"],
                port=int(ES["port"]),
                http_auth=awsauth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection,
                serializer=JSONSerializerPython2()
            )
        else:
            self.es_client = Elasticsearch("{}:{}".format(ES["host"], ES["port"]))

    @staticmethod
    def remove_keyword(query):
        """
        Remove keyword from search term
        """
        query_formatted = query.strip().lower()
        keywords = ['dr', 'dr.', 'doctor', 'nurse', 'co', 'c.o.', 'c.o', 'clinical officer','hf','H.F','health facility']
        for word in keywords:
            regex = r'(?<![\w\d]){0}(?![\w\d])'.format(word)
            query_formatted = re.sub(regex, "", query_formatted)
        return query_formatted.strip()

    def get_from_elasticsearch(self, doc_type, query):
        """
        get data from elasticsearch
        :return: Query results from elasticsearch
        """
        search_term = self.remove_keyword(query)
        results = self.es_client.search(
            index=ES['index'],
            doc_type=doc_type,
            body={
                "query": {
                    "match": {
                        "name": {
                            "query": search_term,
                            "fuzziness": "auto",
                            "prefix_length": 1
                        }
                    }
                }
            }
        )
        return results["hits"]["hits"]