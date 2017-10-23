from flask import Blueprint, redirect
from healthtools.bot import messenger_bot
import requests


blueprint = Blueprint('bot', __name__)

@blueprint.route('/bot/<adapter>', methods=['GET', 'POST'], strict_slashes=False)
def index(adapter='messenger'):
    if requests.method == "POST" :
        return messenger_bot.handle_messages
    else:
        return messenger_bot.handle_verification
        
        
        
