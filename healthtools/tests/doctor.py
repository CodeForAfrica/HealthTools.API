"""
This test for doctors end point
"""
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
        self.assertIn(b"DR NARAYAN VIJAYA KUMAR", response.data)


    def test_doctors_endpoint_gets_doctors(self):
        """
        This tests running doctors endpoint with valid doctype and query
        """
        response = self.client.get("search/doctors?q=john")
        self.assertIn(b"OK", response.data)

    def test_doctors_endpoint_with_bad_endpoint(self):
        """
        This tests running an endpoint with incorrect/unavailable doctype 
        """
        response = self.client.get("search/doctor?q=john")
        self.assertIn(b'"status": "FAILED"', response.data)

class TestDoctorsAPIWithoutDoctype(TestSetup):
    """
    This tests doctors search api without doctype, keywords are used instead
    """
    def test_doctors_endpoint_without_keyword_in_query(self):
        response = self.client.get("search?q=john")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_doctors_endpoint_gets_doctors(self):
        response = self.client.get("search?q=daktari John")
        self.assertIn(b"OK", response.data)

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
