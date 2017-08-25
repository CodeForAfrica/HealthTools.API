from unittest import TestCase
from healthtools_ke_api import app
from healthtools_ke_api.views.search import Elastic

class TestNhifInpatientAPI(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.es = Elastic()
    def test_gets_nhifin_from_elasticsearch(self):
        nhif_inpatient = self.es.get_from_elasticsearch("nhif-inpatient", "ABRAR HEALTH SERVICES LTD")
        self.assertTrue(len(nhif_inpatient) > 0)

    def test_nhifin_endpoint_with_bad_query(self):
        response = self.client.get("/nhif-inpatient/search.json?q=")
        self.assertIn("A query is required.", response.data)

    def test_nhifin_endpoint_gets_nhif_inpatient(self):
        response = self.client.get("/nhif-inpatient/search.json?q=Kenyatta Hsopital")
        self.assertIn("success", response.data)
