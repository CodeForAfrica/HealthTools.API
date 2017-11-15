import logging
from africastalking.AfricasTalkingGateway import (AfricasTalkingGateway, AfricasTalkingGatewayException)
from flask import current_app
from settings import AFRICASTALKING

log = logging.getLogger(__name__)

def send_sms(msg, phone_no):
    username =  AFRICASTALKING['SMS_AFRICASTALKING_USER']
    apikey =  AFRICASTALKING['SMS_AFRICASTALKING_KEY']
    to = phone_no
    message = msg

    results = ''
    gateway = AfricasTalkingGateway(username, apikey)
    
    try:
        results = gateway.sendMessage(to, message)
    except AfricasTalkingGatewayException as e:
        log.error('Encountered an error while sending: %s' ,str(e))
    return results