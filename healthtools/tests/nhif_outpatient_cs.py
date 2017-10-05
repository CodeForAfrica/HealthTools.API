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


class TestNhifOutpatientAPIWithDoctype(TestSetup):
    """
    This tests nhif-outpatient-cs search api with doctype
    """

    def test_nhif_outpatient_cs_endpoint_without_query(self):
        """
        This tests running nhif-outpatient-cs endpoint with valid doctype and no query
        """
        response = self.client.get("search/nhif-outpatient-cs?q=")
        self.assertIn(b"AMIN WOMEN'S CARE CLINIC", response.data)

    def test_nhif_outpatient_cs_endpoint_gets_nhif_outpatient_cs(self):
        """
        This tests running nhif-outpatient-cs endpoint with valid doctype and query
        """
        response = self.client.get("search/nhif-outpatient-cs?q=BRISTOL")
        self.assertIn(b"OK", response.data)

    def test_nhif_outpatient_cs_endpoint_with_bad_endpoint(self):
        """
        This tests running an endpoint with incorrect/unavailable doctype 
        """
        response = self.client.get("search/nhifoutpatient-cs?q=BRISTOL")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_outpatient_cs_endpoint_with_unavailable_query(self):
        """
        This tests running nhif-outpatient-cs endpoint with correct doctype but unavailable query
        """
        response = self.client.get("search/nhif-outpatient-cs?q=1234")
        self.assertIn(b'"status": "FAILED"', response.data)


class TestNhifOutpatientAPIWithoutDoctype(TestSetup):
    """
    This tests nhif-outpatient-cs search api without doctype, keywords are used instead
    """

    def test_nhif_outpatient_cs_endpoint_without_keyword_in_query(self):
        response = self.client.get("search?q=Kenyatta")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_outpatient_cs_endpoint_gets_nhif_outpatient_cs(self):
        response = self.client.get("search?q=bima outpatient-cs Kilifi")
        self.assertIn(b"OK", response.data)

    def test_nhif_outpatient_cs_endpoint_with_unavailable_query(self):
        """
        This tests running nhif-outpatient-cs endpoint with correct available keyword but unavailable query
        """
        response = self.client.get("search?q=outpatient-cs insurance 1234")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_outpatient_cs_endpoint_with_keyword_only(self):
        """
        This tests running nhif-outpatient-cs endpoint with correct available keyword only
        """
        response = self.client.get("search?q=outpatient-cs insurance")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_outpatient_cs_endpoint_without_query(self):
        """
        This tests running nhif-outpatient-cs endpoint without query
        """
        response = self.client.get("search?q=")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhif_outpatient_cs_endpoint_with_nonkeyword(self):
        """
        This tests running nhif-outpatient-cs endpoint with a keyword that is unavailable.
        """
        response = self.client.get("search?q=maji Kilifi")
        self.assertIn(b'"status": "FAILED"', response.data)
