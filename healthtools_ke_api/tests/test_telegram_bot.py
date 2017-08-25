import re
import unittest

from healthtools_ke_api import app
from healthtools_ke_api.views.telegram_bot import telegram_bot as tg

from healthtools_ke_api.settings import DEBUG, TGBOT

DEBUG = False


class TestTelegramBot(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_https_webhook(self):
        """
        Test a https url is provided
        """
        url = re.search("https", TGBOT["BOT_WEBHOOK_URL"])
        self.assertTrue(url)

    def test_invalid_get(self):
        response = self.client.get('/' + TGBOT["BOT_TOKEN"])
        self.assertEqual(response.status_code, 405)
