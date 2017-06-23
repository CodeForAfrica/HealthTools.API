from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from healthtools_ke_api.settings import AWS_CONFIGS as AWS, ES
from serializer import JSONSerializerPython2
import re

class Elastic(object):
    """
    Common class for elastic search client and methods
    """
    def __init__(self):
        # set up authentication credentials
        awsauth = AWS4Auth(AWS["aws_access_key_id"], AWS["aws_secret_access_key"], AWS["region_name"], 'es')
        # client host for aws elastic search service
        if ES['host']:
            self.es_client = Elasticsearch(
                hosts=ES['host'],
                port=443,
                http_auth=awsauth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection,
                serializer=JSONSerializerPython2()
                )
        else:
            self.es_client = Elasticsearch('127.0.0.1')

    @staticmethod
    def remove_keyword(query):
        """
        Remove keyword from search term
        """
        query_formatted = query.strip().lower()
        keywords = ['dr', 'dr.', 'doctor', 'nurse', 'co', 'c.o.', 'c.o', 'clinical officer']
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
                        "name": query
                        }
                    }
                }
            )
        return results["hits"]["hits"]
