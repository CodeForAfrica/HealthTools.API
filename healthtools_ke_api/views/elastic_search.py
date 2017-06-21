from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from healthtools_ke_api.settings import AWS_CONFIGS as AWS, ES
from serializer import JSONSerializerPython2


class Elastic(object):
    """
    Common class for elastic search client and methods
    """
    def __init__(self):
        # set up authentication credentials
        awsauth = AWS4Auth(AWS["aws_access_key_id"], AWS["aws_secret_access_key"], AWS["region_name"], 'es')
        # client host for aws elastic search service
        self.es_client = Elasticsearch(
            hosts=ES['host'],
            port=443,
            http_auth=awsauth,
            use_ssl=True,
            verify_certs=True,
            connection_class=RequestsHttpConnection,
            serializer=JSONSerializerPython2()
            )

    def get_from_elasticsearch(self, doc_type, query):
        """
        get data from elasticsearch
        :return: Query results from elasticsearch
        """
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
