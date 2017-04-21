from unittest import TestCase
from healthtools_ke_api import app
from healthtools_ke_api.nurses import get_nurses_from_nc_registry


class TestNursesAPI(TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_gets_nurses_from_nc_registry(self):
        nurses = get_nurses_from_nc_registry("Marie")
        self.assertTrue(len(nurses) > 0)

    def test_gets_nurses_from_nc_registry_handle_inexistent_nurse(self):
        nurses = get_nurses_from_nc_registry("ihoafiho39023u8")
        self.assertEqual(len(nurses), 0)

    def test_nurses_endpoint_handles_bad_query(self):
        response = self.client.get("/nurses/search.json?q=")
        self.assertIn("A query is required.", response.data)

    def test_nurses_endpoint_gets_nurses(self):
        response = self.client.get("/nurses/search.json?q=Marie")
        self.assertIn("success", response.data)

    def test_nurses_endpoint_can_retrieve_cached_result(self):
        # call once
        self.client.get("/nurses/search.json?q=Marie")
        # second time should retrieve cached result
        response = self.client.get("/nurses/search.json?q=Marie")
        self.assertIn("X-Retrieved-From-Cache", response.headers.keys())
