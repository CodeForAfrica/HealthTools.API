import os

# Url of memcached server
MEMCACHED_URL = os.getenv("MEMCACHED_URL")


class Config(object):
    DEBUG = True
    # Google Analytics tracking id
    GA_TRACKING_ID = os.environ.get('GA_TRACKING_ID')

    # SMS provider credentials
    SMS_USER = os.environ.get('SMS_USER')
    SMS_PASS = os.environ.get('SMS_PASS')
    SMS_SHORTCODE = os.environ.get('SMS_SHORTCODE')

    DOCTORS_SEARCH_URL = "https://6ujyvhcwe6.execute-api.eu-west-1.amazonaws.com/prod"
    NURSE_SEARCH_URL = "https://api.healthtools.codeforafrica.org/nurses/search.json"
    CO_SEARCH_URL = "https://vfblk3b8eh.execute-api.eu-west-1.amazonaws.com/prod"
    NHIF_SEARCH_URL = "https://t875kgqahj.execute-api.eu-west-1.amazonaws.com/prod"
    HF_SEARCH_URL = "https://187mzjvmpd.execute-api.eu-west-1.amazonaws.com/prod"


# development config
class DevConfig(Config):
    THREADED = True
    PORT = 5555
    NURSE_SEARCH_URL = "http://0.0.0.0:5555/nurses/search.json"
