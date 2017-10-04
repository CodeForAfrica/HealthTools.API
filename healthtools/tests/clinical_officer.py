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

class TestClinicalOfficersAPIWithDoctype(TestSetup):
    """
    This tests clinical officers search api with doctype
    """
    #happy path
    
    def test_cos_endpoint_with_bad_query(self):
        """
        This will display all the clinical officers available
        """
        response = self.client.get("search/clinical-officers?q=")
        self.assertIn(b"ELIKANAH KEBAGENDI OMWENGA", response.data)

    #sad path

    def test_cos_endpoint_gets_clinical_officers(self):
        """
        This will display all the clinical officers with the name John
        """
        response = self.client.get("search/clinical-officers?q=john")
        self.assertIn(b"OK", response.data)

class TestClinicalOfficersAPIWithoutDoctype(TestSetup):
    """
    This tests clinical officers search api without doctype keywords are used instead
    """
    def test_cos_endpoint_with_bad_query(self):
        response = self.client.get("search?q=john")
        self.assertIn(b'"status": "FAILED"', response.data)

    def test_cos_endpoint_gets_clinical_officers(self):
        response = self.client.get("search?q=Clinical Officer John")
        self.assertIn(b"OK", response.data)
        self.assertIn(b'"doc_type": "clinical-officers"', response.data)