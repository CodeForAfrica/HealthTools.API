from elasticsearch import helpers
import urllib2, json
from flask.cli import AppGroup

from healthtools.manage import app
from healthtools.core import es, es_index

htools_cli = AppGroup('htools')

@htools_cli.command('loaddata')
def load_data():
    url = 'https://s3-eu-west-1.amazonaws.com/cfa-healthtools-ke/data/doctors.json'
    response = urllib2.urlopen(url)
    helpers.bulk(es, json.load(response), index=es_index, doc_type='doctors')

@htools_cli.command('resetindex')
def reset_index():
    es.indices.delete(index=es_index, ignore=[400, 404])
    es.indices.create(index=es_index, ignore=400)

app.cli.add_command(htools_cli)
