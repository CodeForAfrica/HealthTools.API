from unittest import TestCase
from healthtools_ke_api import app
from healthtools_ke_api.views.search import Elastic


class TestHealthFacilitiesAPI(TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.es = Elastic()

    def test_gets_hf_from_elasticsearch(self):
        health_facility = self.es.get_from_elasticsearch("health-facilities", "Penda Medical Care-Kahawa West")
        self.assertTrue(len(health_facility) > 0)

    def test_hf_endpoint_with_bad_query(self):
        response = self.client.get("/health-facilities/search.json?q=")
        self.assertIn("A query is required.", response.data)

    def test_hf_endpoint_gets_health_facility(self):
        response = self.client.get("/health-facilities/search.json?q=mombasa")
        self.assertIn("success", response.data)
