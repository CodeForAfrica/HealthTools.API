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

class TestNhifOutpatientCSAPI(TestSetup):
    """
    This tests nhif accredited cs outpatient hospitals search api endpoint with  defined doctype
    """
    def test_nhifopcs_endpoint_with_bad_query(self):
        """
        This will display all the hospitals offering nhif outpatient cs available
        """
        response = self.client.get("search/nhif-outpatient-cs?q=")
        self.assertIn(b"ALIF MEDICAL CENTRE", response.data)

    def test_nhifopcs_endpoint_gets_nhif_outpatient_cs(self):
        """
        This will display all the hospitals offering nhif outpatient cs with the name baba dogo
        """
        response = self.client.get("search/nhif-outpatient-cs?q=baba dogo")
        self.assertIn(b"OK", response.data)

class TestNhifOutpatientCSAPIWithoutDoctype(TestSetup):
    """
    This tests nhif accredited cs outpatient hospitals search api endpoint using keyword
    """
    def test_nhifopcs_endpoint_with_bad_query(self):
        response = self.client.get("search?q=Kenyatta")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhifopcs_endpoint_gets_nhif_outpatient_cs(self):
        response = self.client.get("search?q=nhif Kenyatta")
        self.assertIn(b"OK", response.data)