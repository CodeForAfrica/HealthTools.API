from unittest import TestCase
from healthtools_ke_api import app
from healthtools_ke_api.views.clinical_officers import get_clinical_officers_from_cloudsearch


class TestClinicalOfficersAPI(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_gets_cos_from_cloudsearch(self):
        clinical_officers = get_clinical_officers_from_cloudsearch("Marie")
        self.assertTrue(len(clinical_officers) > 0)

    def test_cos_endpoint_with_bad_query(self):
        response = self.client.get("/clinical-officers/search.json?q=")
        self.assertIn("A query is required.", response.data)

    def test_cos_endpoint_gets_doctors(self):
        response = self.client.get("/clinical-officers/search.json?q=Marie")
        self.assertIn("success", response.data)
