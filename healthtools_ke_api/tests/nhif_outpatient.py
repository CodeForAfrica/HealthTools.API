from unittest import TestCase
from healthtools_ke_api import app
from healthtools_ke_api.views.search import Elastic

class TestNhifOutpatientAPI(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.es = Elastic()
    def test_gets_nhifop_from_elasticsearch(self):
        nhif_outpatient = self.es.get_from_elasticsearch("nhif-outpatient", "Jacob")
        self.assertTrue(len(nhif_outpatient) > 0)

    def test_nhifop_endpoint_with_bad_query(self):
        response = self.client.get("/nhif-outpatient/search.json?q=")
        self.assertIn("A query is required.", response.data)

    def test_nhifop_endpoint_gets_nhif_outpatient(self):
        response = self.client.get("/nhif-outpatient/search.json?q=Kenyatta")
        self.assertIn("success", response.data)
