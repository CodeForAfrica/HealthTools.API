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


class TestNhifInpatientAPIWithDoctype(TestSetup):
    """
    This tests nhif-inpatient search api with doctype
    """

    def test_nhif_inpatient_endpoint_without_query(self):
        """
        This tests running nhif-inpatient endpoint with valid doctype and no query
        """
        response = self.client.get("search/nhif-inpatient?q=")
        self.assertIn(b"MARIE STOPES KENYA LIMITED", response.data)

    def test_nhif_inpatient_endpoint_gets_nhif_inpatient(self):
        """
        This tests running nhif-inpatient endpoint with valid doctype and query
        """
        response = self.client.get("search/nhif-inpatient?q=MATHARE")
        self.assertIn(b"OK", response.data)

    def test_nhif_inpatient_endpoint_with_bad_endpoint(self):
        """
        This tests running an endpoint with incorrect/unavailable doctype 
        """
        response = self.client.get("search/nhifinpatient?q=MATHARE")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_inpatient_endpoint_with_unavailable_query(self):
        """
        This tests running nhif-inpatient endpoint with correct doctype but unavailable query
        """
        response = self.client.get("search/nhif-inpatient?q=1234")
        self.assertIn(b'"status": "FAILED"', response.data)


class TestNhifInpatientAPIWithoutDoctype(TestSetup):
    """
    This tests nhif-inpatient search api without doctype, keywords are used instead
    """

    def test_nhif_inpatient_endpoint_without_keyword_in_query(self):
        response = self.client.get("search?q=john")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_inpatient_endpoint_gets_nhif_inpatient(self):
        response = self.client.get("search?q=bima inpatient Kilifi")
        self.assertIn(b"OK", response.data)

    def test_nhif_inpatient_endpoint_with_unavailable_query(self):
        """
        This tests running nhif-inpatient endpoint with correct available keyword but unavailable query
        """
        response = self.client.get("search?q=inpatient insurance 1234")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_inpatient_endpoint_with_keyword_only(self):
        """
        This tests running nhif-inpatient endpoint with correct available keyword only
        """
        response = self.client.get("search?q=inpatient insurance")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_inpatient_endpoint_without_query(self):
        """
        This tests running nhif-inpatient endpoint without query
        """
        response = self.client.get("search?q=")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_inpatient_endpoint_with_nonkeyword(self):
        """
        This tests running nhif-inpatient endpoint with a keyword that is unavailable.
        """
        response = self.client.get("search?q=maji Kilifi")
        self.assertIn(b'"status": "FAILED"', response.data)
