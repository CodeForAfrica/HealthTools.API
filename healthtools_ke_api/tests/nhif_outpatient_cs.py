from unittest import TestCase
from healthtools_ke_api import app
from healthtools_ke_api.views.search import Elastic


class TestNhifOutpatientCSAPI(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.es = Elastic()
    def test_gets_nhifopcs_from_elasticsearch(self):
        nhif_outpatient_cs = self.es.get_from_elasticsearch("nhif-outpatient-cs", "Kenyatta hospital")
        self.assertTrue(len(nhif_outpatient_cs) > 0)

    def test_nhifopcs_endpoint_with_bad_query(self):
        response = self.client.get("/nhif-outpatient-cs/search.json?q=")
        self.assertIn("A query is required.", response.data)

    def test_nhifopcs_endpoint_gets_nhif_outpatient_cs(self):
        response = self.client.get("/nhif-outpatient-cs/search.json?q=Kenyatta")
        self.assertIn("success", response.data)
