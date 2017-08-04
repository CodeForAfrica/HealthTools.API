import json
from django.test import Client, TestCase
from ..views.sms_handler import build_query_response


class TestSmsApi(TestCase):
    def setUp(self):
        self.client = Client()

    def test_sms_requires_message_and_number(self):
        response = self.client.get("/sms/")
        message = "The url parameters 'message' and 'phoneNumber' are required."
        self.assertEqual(message, json.loads(response.content))

    def test_query_response(self):
        response = build_query_response('nurse mary')
        self.assertTrue(len(response[0]) > 0)

    def test_send_sms(self):
        message = build_query_response('nurse mary')
        response = self.client.get("/sms/", query_string={"phoneNumber": "+254726075080", "message": message[0]})
        self.assertEqual(200, response.status_code)

    def test_queries_not_understood_post_to_slack(self):
        message = build_query_response('Test SMS error posts to slack')
        response = self.client.get("/sms/", query_string={"phoneNumber": "+254726075080", "message": message[0]})
        self.assertEqual(200, response.status_code)
