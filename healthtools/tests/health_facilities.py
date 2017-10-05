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
    This tests health-facilities search api with doctype
    """

    def test_health_facilities_endpoint_without_query(self):
        """
        This tests running health-facilities endpoint with valid doctype and no query
        """
        response = self.client.get("search/health-facilities?q=")
        self.assertIn(b"Tamba Pwani", response.data)

    def test_health_facilities_endpoint_gets_health_facilities(self):
        """
        This tests running health-facilities endpoint with valid doctype and query
        """
        response = self.client.get("search/health-facilities?q=eldoret")
        self.assertIn(b"OK", response.data)

    def test_health_facilities_endpoint_with_bad_endpoint(self):
        """
        This tests running an endpoint with incorrect/unavailable doctype 
        """
        response = self.client.get("search/healthfacilities?q=Kitale")
        self.assertIn(b'"status": "FAILED"', response.data)


class TestHealthFacilitiesAPIWithoutDoctype(TestSetup):
    """
    This tests health-facilities search api without doctype, keywords are used instead
    """

    def test_health_facilities_endpoint_without_keyword_in_query(self):
        response = self.client.get("search?q=kakamega")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_health_facilities_endpoint_gets_health_facilities(self):
        response = self.client.get("search?q=dispensary Kilifi")
        self.assertIn(b"OK", response.data)

    def test_health_facilities_endpoint_with_keyword_only(self):
        """
        This tests running health-facilities endpoint with correct available keyword only
        """
        response = self.client.get("search?q=hf")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_health_facilities_endpoint_without_query(self):
        """
        This tests running health-facilities endpoint without query
        """
        response = self.client.get("search?q=")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_health_facilities_endpoint_with_nonkeyword(self):
        """
        This tests running health-facilities endpoint with a keyword that is unavailable.
        """
        response = self.client.get("search?q=maji Mombasa")
        self.assertIn(b'"status": "FAILED"', response.data)
