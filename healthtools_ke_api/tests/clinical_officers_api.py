from unittest import TestCase
from healthtools_ke_api import app
from healthtools_ke_api.views.search import Elastic


class TestClinicalOfficersAPI(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.es = Elastic()

    def test_gets_cos_from_elasticsearch(self):
        clinical_officers = self.es.get_from_elasticsearch("clinical-officers", "Jacob")
        self.assertTrue(len(clinical_officers) > 0)

    def test_cos_endpoint_with_bad_query(self):
        response = self.client.get("/clinical-officers/search.json?q=")
        self.assertIn("A query is required.", response.data)

    def test_cos_endpoint_gets_clinical_officers(self):
        response = self.client.get("/clinical-officers/search.json?q=Ann")
        self.assertIn("success", response.data)
