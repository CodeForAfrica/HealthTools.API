import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import unittest
from healthtools.manage import app
from healthtools.search.nurses import get_nurses_from_nc_registry

class TestSetup(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

class TestNurseRegistery(TestSetup):
    """
    This tests nurses search api with defined doctype
    """
    def test_gets_nurses_from_nc_registry(self):
        nurses = get_nurses_from_nc_registry("Marie")
        self.assertTrue(len(nurses) > 0)

    def test_gets_nurses_from_nc_registry_handle_inexistent_nurse(self):
        nurses = get_nurses_from_nc_registry("ihoafiho39023u8")
        self.assertEqual(len(nurses), 0)
        self.assertIn
    

class TestNursesAPI(TestSetup):
    """
    This tests nurses search api with defined doctype
    """
    def test_nurses_endpoint_handles_bad_query(self):
        response = self.client.get("search/nurses?q=")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nurses_endpoint_gets_nurses(self):
        response = self.client.get("search/nurses?q=Marie")
        self.assertIn(b"OK", response.data)

    def test_nurses_endpoint_can_retrieve_cached_result(self):
        # call once
        self.client.get("search/nurses?q=Marie")
        # second time should retrieve cached result
        response = self.client.get("search/nurses?q=Marie")
        self.assertIn(b"X-Retrieved-From-Cache", response.headers.keys())

class TestNursesAPIWithoutDoctypes(TestSetup):
    """
    This tests nurses search api using keywords
    """
    def test_nurses_endpoint_handles_bad_query(self):
        response = self.client.get("search?q=Marie")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nurses_endpoint_gets_nurses(self):
        response = self.client.get("search?q=nurse Marie")
        self.assertIn(b"OK", response.data)
        self.assertIn(b"MARIE   WANJUGU  MURIGO", response.data)
    
