"""
This test for nhif outpatient end point
"""
import unittest
from healthtools.manage import app


class TestSetup(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()


class TestNhifOutpatientAPIWithDoctype(TestSetup):
    """
    This tests nhif-outpatient search api with doctype
    """

    def test_nhif_outpatient_endpoint_without_query(self):
        """
        This tests running nhif-outpatient endpoint with valid doctype and no query
        """
        response = self.client.get("search/nhif-outpatient?q=")
        self.assertIn(b"AMIN WOMEN'S CARE CLINIC", response.data)

    def test_nhif_outpatient_endpoint_gets_nhif_outpatient(self):
        """
        This tests running nhif-outpatient endpoint with valid doctype and query
        """
        response = self.client.get("search/nhif-outpatient?q=BRISTOL")
        self.assertIn(b"OK", response.data)

    def test_nhif_outpatient_endpoint_with_bad_endpoint(self):
        """
        This tests running an endpoint with incorrect/unavailable doctype 
        """
        response = self.client.get("search/nhifoutpatient?q=BRISTOL")
        self.assertIn(b'"status": "FAILED"', response.data)


class TestNhifOutpatientAPIWithoutDoctype(TestSetup):
    """
    This tests nhif-outpatient search api without doctype, keywords are used instead
    """

    def test_nhif_outpatient_endpoint_without_keyword_in_query(self):
        response = self.client.get("search?q=Kenyatta")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_outpatient_endpoint_gets_nhif_outpatient(self):
        response = self.client.get("search?q=bima outpatient Kilifi")
        self.assertIn(b"OK", response.data)

    def test_nhif_outpatient_endpoint_with_keyword_only(self):
        """
        This tests running nhif-outpatient endpoint with correct available keyword only
        """
        response = self.client.get("search?q=outpatient insurance")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_outpatient_endpoint_without_query(self):
        """
        This tests running nhif-outpatient endpoint without query
        """
        response = self.client.get("search?q=")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_outpatient_endpoint_with_nonkeyword(self):
        """
        This tests running nhif-outpatient endpoint with a keyword that is unavailable.
        """
        response = self.client.get("search?q=maji Kilifi")
        self.assertIn(b'"status": "FAILED"', response.data)
