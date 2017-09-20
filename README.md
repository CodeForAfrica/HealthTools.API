# HealthTools.API

The HealthTools API. Providing actionable health information.

Our data sources include: 

- Doctors: http://medicalboard.co.ke/online-services/retention/
- Foreign doctors: http://medicalboard.co.ke/online-services/foreign-doctors-license-register
- Clinical officers: http://clinicalofficerscouncil.org/online-services/retention/

The scrapers for this data can be found here:

- ?

## Usage

Specification for the API is shown below. It is an open api and requires no authentication to access.


| EndPoint                            | Allowed Methods  | Functionality                                            | Parameters |
|-------------------------------------|------------------|----------------------------------------------------------|------------|
| `/doctors/search.json`              | GET              | Search a doctor by the name                              | q=[name]   |
| `/nurses/search.json`               | GET              | Search a nurse by the name                               | q=[name]   |
| `/clinical-officers/search.json`    | GET              | Search a clinical officer by the name                    | q=[name]   |


## Installation

Clone the repo from github `$ git clone git@github.com:RyanSept/HealthTools.KE-api.git`

Change directory into package `$ cd HealthTools.KE-api`

Install the dependencies by running `$ pip install -r requirements.txt`

Install Memcached
 * If on linux follow this [link](https://github.com/memcached/memcached/wiki/Install)
 * On mac use `brew install memcached`

You can set the required environment variables like so
```<>
$ export APP_DEBUG=<False> # True or False
$ export MEMCACHED_URL=<memcache_url:port> # defaults to 127.0.0.1:8000
$ export GA_TRACKING_ID=<google-analytics-tracking-id>
$ export SMS_USER=<sms-provider-user-id>
$ export SMS_PASS=<sms-provider-passcode>
$ export SMS_SHORTCODE=<sms-provider-shortcode>
$ export SMS_SEND_URL=<url-for-sms-provider>
$ export AWS_ACCESS_KEY=<aws-access-key-id>
$ export AWS_SECRET_KEY=<aws-secret-key>
$ export ES_HOST=<elasticsearch_host_endpoint> (DO NOT SET THIS IF YOU WOULD LIKE TO USE ELASTIC SEARCH LOCALLY ON YOUR MACHINE)
$ export ES_PORT=<elasticsearch_port>
$ export ES_INDEX=<elasticsearch_index>

# Telegram Bot required environment variables
export BOT_TOKEN=<telegram-bot-token-assigned-by-BotFather>

# Note: Telegram Bot only works with HTTPS
export BOT_WEBHOOK_URL=<https-forwarding-address-from-ngrok>
export SERVER_IP="localhost"
export TELEGRAM_PORT=5000

# openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 3650 -out cert.pem
export CERT_FILE=</path/to/cert/file>
export KEY_FILE=</path/to/keu/file>
```
**If you want to use elasticsearch locally on your machine use the following instructions to set it up**

For linux and windows users, follow instructions from this [link](https://www.elastic.co/guide/en/elasticsearch/reference/current/setup.html)

For mac users run `brew install elasticsearch` on your terminal

Run memcached on your terminal `$ memcached -p <port you set MEMCACHED_URL to run on>(default: 8000)`

If you set up elasticsearch locally run it `$ elasticsearch`

You can now run the server `$ python manage.py` or `gunicorn manage:app` for production.

# Setting up Telegram Bot on HealthTools.KE-api
The Telegram Bot does the followinng:
1. Check to see if your doctor, nurse, or clinical officer is registered
2. Find out which facilities your NHIF card will cover in your county
3. Find the nearest doctor or health facility

**Installation**
Make sure you have installed in your environment: `python-telegram-bot`

**Create a new telegram bot**
- Use [BotFather](https://telegram.me/BotFather)
- After you create your bot, save the token assigned.

**ngrok Configuration**
- ngrok allows you to expose a web server running on your local machine to the interne
- Install Ngrok: https://ngrok.com
- Follow the setup instructions [here](https://ngrok.com/docs#expose)
    Note: The listening port you use, is the same one your app should listen on. E.g.
    ```$ ngrok http 5000```

    In manage.py:
    ```
    if __name__ == '__main__':
        app.run(
            host="localhost", # Since ngrok is running locally
            port=5000, # the app listens on the same port as ngrok
        )
    ```

**Nginx Configuration**
- Install Nginx
    https://www.nginx.com/resources/admin-guide/installing-nginx-open-source/
    or
    for mac users: https://coderwall.com/p/dgwwuq/installing-nginx-in-mac-os-x-maverick-with-homebrew

- Configuration
    https://www.nginx.com/resources/wiki/start/topics/examples/full/
    Ensure you add `proxy_set_header    X-Forwarded-Proto https;` in location since Telegram bot webhooks works *only* with HTTPS URLs

### Tests

Run memcached on your terminal `$ memcached -p <port you set MEMCACHED_URL to run on>(default: 8000)`

_**make sure if you use elasticsearch locally, it's running**_

Use nosetests to run tests (with stdout) like this:
```$ nosetests --nocapture```



## Contributing

?

---

## License

?
