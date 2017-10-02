import os
import inspect
import sys
currentdir = os.path.dirname(os.path.abspath(
    inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)
import unittest
from healthtools.manage import app
class TestSetup(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

class TestHealthFacilitiesAPIWithDoctype(TestSetup):
    """
    This tests Health Facilities search api with doctype
    """
    def test_hf_endpoint_with_bad_query(self):
        """
        This will display all the health facilities available
        """
        response = self.client.get("search/health-facilities?q=")
        self.assertIn(b"Kituni Dispensary", response.data)

    def test_hf_endpoint_gets_health_facilities(self):
        """
        This will display All the health facilities with the name penda
        """
        response = self.client.get("search/health-facilities?q=penda")
        self.assertIn(b"OK", response.data)

class TestHealthFacilitiesAPIWithoutDoctype(TestSetup):
    """
    This tests Health Facilities search api without doctype
    A key word should be used for a succesfull response
    """
    def test_hf_endpoint_with_bad_query(self):
        response = self.client.get("search?q=penda")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_hf_endpoint_gets_health_facilities(self):
        response = self.client.get("search?q=hf penda")
        self.assertIn(b"OK", response.data)
        self.assertIn(b'"doc_type": "health-facilities"', response.data)
