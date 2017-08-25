import re
import unittest

from healthtools_ke_api import app
from healthtools_ke_api.views.telegram_bot import telegram_bot as tg

from healthtools_ke_api.settings import DEBUG, TGBOT

DEBUG = False


class TestTelegramBot(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        msg = {
            "update_id": 865272811,
            "message": {
                "message_id": 83,
                "from": {
                    "id": 346670031,
                    "is_bot": "false",
                    "first_name": "Tina",
                    "language_code": "en-KE"
                },
                "chat": {
                    "id": 346670031,
                    "first_name": "Tina",
                    "type": "private"
                },
                "date": 1503566582,
                "text": "/start",
                "entities": [
                    {
                        "offset": 0,
                        "length": 6,
                        "type": "bot_command"
                    }
                ]
            }
        }

    # TGBOT = {
    #     "BOT_TOKEN": os.getenv('BOT_TOKEN'),
    #     "SERVER_IP": os.getenv("SERVER_IP"),
    #     "TELEGRAM_PORT": os.getenv("TELEGRAM_PORT", 8443),
    #     "CERT_FILE": os.getenv("CERT_FILE"),
    #     "KEY_FILE": os.getenv("KEY_FILE"),
    #     "BOT_WEBHOOK_URL": os.getenv("BOT_WEBHOOK_URL")
    # }

    def test_https_webhook(self):
        """
        Test a https url is provided
        """
        url = re.search("https", TGBOT["BOT_WEBHOOK_URL"])
        self.assertTrue(url)

    def test_invalid_get(self):
        response = self.client.get('/' + TGBOT["BOT_TOKEN"])
        self.assertEqual(response.status_code, 405)
