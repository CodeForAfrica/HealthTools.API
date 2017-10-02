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
    This tests nhif accredited inpatient hospitals search api endpoint with a defined doctype
    """
    def test_nhifin_endpoint_with_bad_query(self):
        """
        This will display all the nhif inpatient hospitals available
        """
        response = self.client.get("/search/nhif-inpatient?q=")
        self.assertIn("FAMILY HEALTH OPTIONS", response.data)

    def test_nhifin_endpoint_gets_nhif_inpatient(self):
        """
        This will display All the nhif inpatient hospitals  with the name edelvale
        """
        response = self.client.get("/search/nhif-inpatient?q=EDELVALE")
        self.assertIn("OK", response.data)

class TestNhifInpatientAPIWithoutDoctype(TestSetup):
    """
    This tests nhif inpatient api endpoint using keywords
    """
    def test_nhifin_endpoint_with_bad_query(self):
        response = self.client.get("search?q=EDELVALE")
        self.assertIn('"status": "FAILED"', response.data)

    def test_nhifin_endpoint_gets_nhif_inpatient(self):
        response = self.client.get("search?q=nhif inpatient EDELVALE")
        self.assertIn("OK", response.data)
        self.assertIn(' "doc_type": "nhif-inpatient"', response.data)


