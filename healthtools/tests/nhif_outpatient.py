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

class TestNhifOutpatientAPI(TestSetup):
    """
    This tests search nhif accredited outpatient hospitals search api endpoint with doctype
    """
    def test_nhifop_endpoint_with_bad_query(self):
        """
        This will display all the nhif accredited outpatient hospitals available
        """
        response = self.client.get("search/nhif-outpatient?q=")
        self.assertIn(b"CANCER CARE INTERNATIONAL", response.data)

    def test_nhifop_endpoint_gets_nhif_outpatient(self):
        """
        This will display all the nhif accredited outpatient hospitals with the name bristol park
        """
        response = self.client.get("search/nhif-outpatient?q=bristol park")
        self.assertIn(b"OK", response.data)

class TestNhifOutpatientAPIWithoutDoctype(TestSetup):
    """
    This tests search nhif accredited outpatient hospitals search api endpoint using keywords
    """
    def test_nhifop_endpoint_with_bad_query(self):
        response = self.client.get("search?q=Kenyatta")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_nhifop_endpoint_gets_nhif_outpatient(self):
        response = self.client.get("search?q=nhif Kenyatta")
        self.assertIn(b"OK", response.data)
        self.assertIn(b'"doc_type": "nhif-outpatient"', response.data)
    
