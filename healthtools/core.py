import logging

from werkzeug.local import LocalProxy
from flask import Flask, current_app
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

from healthtools import settings


log = logging.getLogger(__name__)


def create_app(config={}):
    app = Flask('healthtools')
    app.config.from_object(settings)
    app.config.update(config)
    app_name = app.config.get('APP_NAME')

    # TODO: Add Slack error log handler here

    return app


def get_es():
    app = current_app._get_current_object()
    if not hasattr(app, '_es_instance'):
        if 'aws' in app.config.get('ELASTICSEARCH_HOST'):
            host = app.config.get('ELASTICSEARCH_HOST')
            awsauth = AWS4AuthNotUnicode(app.config.get('AWS_ACCESS_KEY'),
                                         app.config.get('AWS_SECRET_KEY'),
                                         app.config.get('AWS_REGION'),
                                         'es')
            app._es_instance = Elasticsearch(
                hosts=[{'host': host, 'port': 443}],
                http_auth=awsauth,
                use_ssl=True,
                verify_certs=True,
                connection_class=RequestsHttpConnection,
                timeout=120
            )
        else:
            app._es_instance = Elasticsearch(
                app.config.get('ELASTICSEARCH_HOST'),
                timeout=120
            )
    return app._es_instance


def get_es_index():
    app = current_app._get_current_object()
    return app.config.get('ELASTICSEARCH_INDEX')


es = LocalProxy(get_es)
es_index = LocalProxy(get_es_index)


# Work-around: https://github.com/sam-washington/requests-aws4auth/issues/24

class AWS4AuthNotUnicode(AWS4Auth):
    def __call__(self, req):
        req = super(AWS4AuthNotUnicode, self).__call__(req)
        req.headers = {str(name): value for name, value in req.headers.items()}
        return req
