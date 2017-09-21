import os

DEBUG = os.getenv("APP_DEBUG", False)

# Amazon Web Services configs
AWS_ACCESS_KEY = os.getenv("HTOOLS_AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("HTOOLS_AWS_SECRET_KEY")
AWS_REGION = os.getenv("HTOOLS_AWS_REGION", "eu-west-1")


# Elastic Search configs

ELASTICSEARCH_HOST = os.getenv("HTOOLS_ES_HOST", "127.0.0.1")
ELASTICSEARCH_PORT = os.getenv("HTOOLS_ES_PORT", "9200")
ELASTICSEARCH_INDEX = os.getenv("HTOOLS_ES_INDEX", "healthtools-dev")


# TODO: Updates needed below

# Google Analytics tracking id
GA_TRACKING_ID = os.environ.get("HTOOLS_GA_TRACKING_ID", "UA-44795600-33")


# Url of memcached server
MEMCACHED_URL = os.getenv("HTOOLS_MEMCACHED_URL", "127.0.0.1:11211")


# SMS provider credentials
SMS_USER = os.environ.get("HTOOLS_SMS_USER")
SMS_PASS = os.environ.get("HTOOLS_SMS_PASS")
SMS_SHORTCODE = os.environ.get("HTOOLS_SMS_SHORTCODE")


# TGBOT: TElegram Bot
TGBOT = {
    "BOT_TOKEN": os.getenv("BOT_TOKEN"),
    "SERVER_IP": os.getenv("SERVER_IP"),
    "TELEGRAM_PORT": os.getenv("TELEGRAM_PORT", 5000),
    "CERT_FILE": os.getenv("CERT_FILE"),
    "KEY_FILE": os.getenv("KEY_FILE"),
    "BOT_WEBHOOK_URL": os.getenv("HTOOLS_BOT_WEBHOOK_URL")
}

SLACK_URL = os.getenv("HTOOLS_SLACK_URL")
