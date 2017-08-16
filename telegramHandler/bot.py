import sys
import os

from webapp2 import WSGIApplication, Route

TOKEN = os.getenv("BOT_TOKEN")

routes = [
    # Route for handle webhook (change it using admin rights, maybe..
    Route('/set_webhook',
          handler='telegramHandler.hook_handler.WebHookHandler:set_webhook'),

    # Route for Telegram updates
    Route('/' + TOKEN, handler='telegramHandler.hook_handler.WebHookHandler:webhook_handler')

]
bot_app = WSGIApplication(routes, debug=False)
