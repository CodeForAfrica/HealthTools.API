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

class TestWithDoctype(TestSetup):
    """
    This tests doctors search api with defined doctype
    """
    def test_doctors_endpoint_with_bad_query(self):
        """
        This will display all the doctors available
        """
        response = self.client.get("/search/doctors?q=")
        self.assertIn(b"DR BAL RAJPREET KAUR", response.data)

    def test_doctors_endpoint_gets_doctors(self):
        """
        This will display All the doctors with the name John
        """
        response = self.client.get("/search/doctors?q=john")
        self.assertIn(b"OK", response.data)

class TestDoctorsAPI(TestSetup):
    """
    This tests doctors search api using keywords
    """
    def test_doctors_endpoint_with_bad_query(self):
        response = self.client.get("search?q=john")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_doctors_endpoint_gets_doctors(self):
        response = self.client.get("search?q=dr john")
        self.assertIn(b"OK", response.data)
        self.assertIn(b' "doc_type": "doctors"', response.data)



