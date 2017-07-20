from django.test import Client, TestCase
from ..elastic import Elastic


class TestClinicalOfficersAPI(TestCase):
    def setUp(self):
        self.client = Client()
        self.es = Elastic()

    def test_gets_cos_from_elasticsearch(self):
        clinical_officers = self.es.get_from_elasticsearch("clinical-officers", "Jacob")
        self.assertTrue(len(clinical_officers) > 0)

    def test_cos_endpoint_with_bad_query(self):
        response = self.client.get("/clinical-officers/search.json?q=")
        self.assertIn("A query is required.", response.content)

    def test_cos_endpoint_gets_doctors(self):
        response = self.client.get("/clinical-officers/search.json?q=Ann")
        self.assertIn("success", response.content)
