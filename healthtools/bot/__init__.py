import logging

from healthtools.bot import facebook_messenger
from healthtools.bot.telegram import telegram_reply
from healthtools.search import run_query

log = logging.getLogger(__name__)

def process_bot_query(query, adapter):
    if (adapter == 'facebook'):
        pass
    else:
        pass

def create_response(result, doctype):
    pass