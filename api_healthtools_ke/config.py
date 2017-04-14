import os

NURSING_COUNCIL_URL = "http://nckenya.com/services/search.php?p=1&s={}"

# Url of memcached server
MEMCACHED_URL = os.getenv("MEMCACHED_URL")

# Google Analytics tracking id
GA_TRACKING_ID = os.environ.get('GA_TRACKING_ID')

# SMS provider credentials
SMS_USER = os.environ.get('SMS_USER')
SMS_PASS = os.environ.get('SMS_PASS')
SMS_SHORTCODE = os.environ.get('SMS_SHORTCODE')
