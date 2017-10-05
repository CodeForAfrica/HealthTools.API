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


class TestNursesAPI(TestSetup):
    """
    This tests nurses search api with defined doctype
    """

    def test_nurses_endpoint_handles_bad_query(self):
        """
        This tests running nurses endpoint with valid doctype and no query
        """
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

    def test_nurses_endpoint_with_bad_endpoint(self):
        """
        This tests running an endpoint with incorrect/unavailable doctype 
        """
        response = self.client.get("search/nurse?q=Marie")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nurses_endpoint_with_unavailable_query(self):
        """
        This tests running nurses endpoint with correct doctype but unavailable query
        """
        response = self.client.get("search/nurses?q=1234")
        self.assertIn(b'"status": "FAILED"', response.data)

class TestNursesAPIWithoutDoctypes(TestSetup):
    """
    This tests nurses search api without doctype, keywords are used instead
    """
    def test_nurses_endpoint_endpoint_without_keyword_in_query(self):
        response = self.client.get("search?q=Marie")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nurses_endpoint_gets_nurses(self):
        response = self.client.get("search?q=nurse Marie")
        self.assertIn(b"OK", response.data)
        self.assertIn(b"MARIE   WANJUGU  MURIGO", response.data)

    def test_nurses_endpoint_with_unavailable_query(self):
        """
        This tests running nurses endpoint with correct available keyword but unavailable query
        """
        response = self.client.get("search?q=Registered Nurse 1234")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nurses_cs_endpoint_with_keyword_only(self):
        """
        This tests running nurses endpoint with correct available keyword only
        """
        response = self.client.get("search?q=nursing officer")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nurses_endpoint_without_query(self):
        """
        This tests running nurses endpoint without query
        """
        response = self.client.get("search?q=")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nurses_endpoint_with_nonkeyword(self):
        """
        This tests running nurses endpoint with a keyword that is unavailable.
        """
        response = self.client.get("search?q=kijana Marie")
        self.assertIn(b'"status": "FAILED"', response.data)

    
