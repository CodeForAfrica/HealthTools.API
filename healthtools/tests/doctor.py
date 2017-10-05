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

class TestDoctorsAPIWithDoctype(TestSetup):
    """
    This tests doctors search api with doctype
    """
    
    def test_doctors_endpoint_without_query(self):
        """
        This tests running doctors endpoint with valid doctype and no query
        """
        response = self.client.get("search/doctors?q=")
        self.assertIn(b"ELIKANAH KEBAGENDI OMWENGA", response.data)


    def test_doctors_endpoint_gets_clinical_officers(self):
        """
        This tests running doctors endpoint with valid doctype and query
        """
        response = self.client.get("search/doctors?q=john")
        self.assertIn(b"OK", response.data)

    def test_doctors_endpoint_with_bad_endpoint(self):
        """
        This tests running an endpoint with incorrect/unavailable doctype 
        """
        response = self.client.get("search/clinicalofficers?q=john")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_doctors_endpoint_with_unavailable_query(self):
        """
        This tests running doctors endpoint with correct doctype but unavailable query
        """
        response = self.client.get("search/doctors?q=1234")
        self.assertIn(b'"status": "FAILED"', response.data)

class TestDoctorsAPIWithoutDoctype(TestSetup):
    """
    This tests doctors search api without doctype, keywords are used instead
    """
    def test_doctors_endpoint_without_keyword_in_query(self):
        response = self.client.get("search?q=john")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_doctors_endpoint_gets_clinical_officers(self):
        response = self.client.get("search?q=daktari John")
        self.assertIn(b"OK", response.data)
    
    def test_doctors_endpoint_with_unavailable_query(self):
        """
        This tests running doctors endpoint with correct available keyword but unavailable query
        """
        response = self.client.get("search?q= daktari 1234")
        self.assertIn(b'"status": "FAILED"', response.data)

    
    def test_doctors_endpoint_with_keyword_only(self):
        """
        This tests running doctors endpoint with correct available keyword only
        """
        response = self.client.get("search?q=daktari")
        self.assertIn(b'"status": "FAILED"', response.data)


    def test_doctors_endpoint_without_query(self):
        """
        This tests running doctors endpoint without query
        """
        response = self.client.get("search?q=")
        self.assertIn(b'"status": "FAILED"', response.data)


    def test_doctors_endpoint_with_nonkeyword(self):
        """
        This tests running doctors endpoint with a keyword that is unavailable.
        """
        response = self.client.get("search?q=maji john")
        self.assertIn(b'"status": "FAILED"', response.data)
