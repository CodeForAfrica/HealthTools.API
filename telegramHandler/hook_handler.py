import json
import telegram
from telegram import bot

from webapp2 import RequestHandler

from telegramHandler.command_handler import TOKEN, webhook, setup, bot

APP_URL = "127.0.0.0:5000"

class WebHookHandler(RequestHandler):
    def set_webhook(self):
        '''
        Set webhook for your bot
        '''
        setup()
        s = bot.setWebhook(APP_URL + '/' + TOKEN)
        if s:
            self.response.write("Webhook set")
        else:
            self.response.write("Webhook setup failed")

    def webhook_handler(self):
        # Retrieve the message in JSON and then transform it to Telegram object
        body = json.loads(self.request.body)
        update = telegram.Update.de_json(body)
        webhook(update)
