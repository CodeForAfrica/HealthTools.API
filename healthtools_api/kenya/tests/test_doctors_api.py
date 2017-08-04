from django.test import Client, TestCase
from ..elastic import Elastic


class TestDoctorsAPI(TestCase):
    def setUp(self):
        self.client = Client()
        self.es = Elastic()

    def test_gets_doctors_from_elasticsearch(self):
        doctors = self.es.get_from_elasticsearch("doctors", "BHATT")
        self.assertTrue(len(doctors) > 0)

    def test_doctors_endpoint_with_bad_query(self):
        response = self.client.get("/doctors/search.json?q=")
        self.assertIn("A query is required.", response.content)

    def test_doctors_endpoint_gets_doctors(self):
        response = self.client.get("/doctors/search.json?q=Marie")
        self.assertIn("success", response.content)
