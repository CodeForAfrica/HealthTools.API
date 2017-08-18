import logging
import os
import re
import requests
import string

from flask import Blueprint, request, current_app
from telegram import Update

from bot_manager import Manager, TOKEN

telegram_bot = Blueprint("telegram_bot", __name__)
manager = Manager(TOKEN)

@telegram_bot.route('/telegram', methods=['GET', 'POST'])
def webhook_handler():
    if request.method == "POST":
        # retrieve the message in JSON and then transform it to Telegram object
        update = Update.de_json(request.get_json(force=True))
        # Update.de_json(json.loads(text))

        chat_id = update.message.chat.id

        # Telegram understands UTF-8, so encode text for unicode compatibility
        text = update.message.text.encode('utf-8')

        # repeat the same message back (echo)
        
        manager.bot.sendMessage(chat_id=chat_id, text=text)

    return 'ok'

@telegram_bot.route('/', methods=['GET', 'POST'])
def set_webhook():
    manager.setup()
