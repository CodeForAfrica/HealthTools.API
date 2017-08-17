from unittest import TestCase
from healthtools_ke_api import app
from healthtools_ke_api.views.search import Elastic


class TestDoctorsAPI(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.es = Elastic()

    def test_gets_doctors_from_elasticsearch(self):
        doctors = self.es.get_from_elasticsearch("doctors", "BHATT")
        self.assertTrue(len(doctors) > 0)

    def test_doctors_endpoint_with_bad_query(self):
        response = self.client.get("/doctors/search.json?q=")
        self.assertIn("A query is required.", response.data)

    def test_doctors_endpoint_gets_doctors(self):
        response = self.client.get("/doctors/search.json?q=Marie")
        self.assertIn("success", response.data)
