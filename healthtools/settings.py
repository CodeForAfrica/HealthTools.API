import os


# Show error messages to the user.
DEBUG = os.getenv('APP_DEBUG', False)

###############################################################################
# General instance information

APP_TITLE = os.getenv('HTOOLS_APP_TITLE', 'HealthTools.API')
APP_NAME = os.getenv('HTOOLS_APP_NAME', 'healthtools')
APP_BASEURL = os.getenv('HTOOLS_APP_URL', 'http://localhost:5000/')

# Force HTTPS here:
PREFERRED_URL_SCHEME = os.getenv('HTOOLS_URL_SCHEME', 'http')


# Amazon Web Services configs
AWS_ACCESS_KEY = os.getenv('HTOOLS_AWS_ACCESS_KEY')
AWS_SECRET_KEY = os.getenv('HTOOLS_AWS_SECRET_KEY')
AWS_REGION = os.getenv('HTOOLS_AWS_REGION', 'eu-west-1')


# Elastic Search configs

ELASTICSEARCH_HOST = os.getenv('HTOOLS_ES_HOST', '127.0.0.1')
ELASTICSEARCH_PORT = os.getenv('HTOOLS_ES_PORT', '9200')
ELASTICSEARCH_INDEX = os.getenv('HTOOLS_ES_INDEX', 'healthtools-dev')


# TODO: Updates needed below

# Google Analytics tracking id
GA_TRACKING_ID = os.getenv('HTOOLS_GA_TRACKING_ID', 'UA-44795600-33')


# Url of memcached server
MEMCACHED_URL = os.getenv('HTOOLS_MEMCACHED_URL', '127.0.0.1:11211')

###############################################################################
# SMS provider credentials

SMS_MTECH_USER = os.getenv('HTOOLS_SMS_MTECH_USER')
SMS_MTECH_PASS = os.getenv('HTOOLS_SMS_MTECH_PASS')
SMS_MTECH_SHORTCODE = os.getenv('HTOOLS_SMS_MTECH_SHORTCODE', '22495')


# TGBOT: TElegram Bot
TGBOT = {
    'BOT_TOKEN': os.getenv('BOT_TOKEN'),
    'SERVER_IP': os.getenv('SERVER_IP'),
    'TELEGRAM_PORT': os.getenv('TELEGRAM_PORT', 5000),
    'CERT_FILE': os.getenv('CERT_FILE'),
    'KEY_FILE': os.getenv('KEY_FILE'),
    'BOT_WEBHOOK_URL': os.getenv('HTOOLS_BOT_WEBHOOK_URL')
}

SLACK_URL = os.getenv('HTOOLS_SLACK_URL')

# Facebook messenger bot tokens
VERIFY_TOKEN = 'EAAb02ovr13sBADIlYFAHuEP6pNKlIyglLZCP5R3oGCfCJrh1aReDbi9qPYNilJPcs3kZBMUNfO036zC6CraGUSE0HRLlkwYn0PRLW7ZBA7keYCfOZB9FFkvZBY2yeAf4h9UhTqHQiHDj1FbxpNlyTWNuZCZAen8aUbKSkkuq23ZAr1bfd27W8vteCVV3GDH2wXoZD'
ACCESS_TOKEN = 'EAAb02ovr13sBADnkA3KB4QHR6iWCZBlgCCnoLo6lPfsPiFtmDXYUhMsJmzlOOdzW8KqaMPZAZCzboW1zDJbOSdkOYDFIsQq7tZCeT5DOfl4rsNhKfPVZCtB3EtggKgMQnuZAKOZAn7EhGx2UrydHVrRw9pSavRZBvmO0kS5fx2sGPMlYgtcyYUMgefuu98UfWHUZD'
