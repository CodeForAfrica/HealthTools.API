import os

DEBUG = os.getenv("APP_DEBUG", False)

# Url of memcached server
MEMCACHED_URL = os.getenv("MEMCACHED_URL", "127.0.0.1:11211")

# Amazon Web Services configs
AWS = {
    "access_key": os.getenv("AWS_ACCESS_KEY"),
    "secret_key": os.getenv("AWS_SECRET_KEY"),
    "region": os.getenv("AWS_REGION", "eu-west-1"),
}

# Elastic Search configs
ES = {
    "host": os.getenv("ES_HOST", "127.0.0.1"),
    "port": os.getenv("ES_PORT", "9200"),
    "index": os.getenv("ES_INDEX", "healthtools-ke")
}

# Google Analytics tracking id
GA_TRACKING_ID = os.environ.get("GA_TRACKING_ID", "UA-44795600-33")

# SMS provider credentials
SMS_USER = os.environ.get("SMS_USER")
SMS_PASS = os.environ.get("SMS_PASS")
SMS_SHORTCODE = os.environ.get("SMS_SHORTCODE")
