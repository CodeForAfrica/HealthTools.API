from unittest import TestCase
from healthtools_ke_api import app
from healthtools_ke_api.views.doctors import get_doctors_from_cloudsearch


class TestNursesAPI(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_gets_doctors_from_cloudsearch(self):
        doctors = get_doctors_from_cloudsearch("Marie")
        self.assertTrue(len(doctors) > 0)

    def test_doctors_endpoint_with_bad_query(self):
        response = self.client.get("/doctors/search.json?q=")
        self.assertIn("A query is required.", response.data)

    def test_doctors_endpoint_gets_doctors(self):
        response = self.client.get("/doctors/search.json?q=Marie")
        self.assertIn("success", response.data)
