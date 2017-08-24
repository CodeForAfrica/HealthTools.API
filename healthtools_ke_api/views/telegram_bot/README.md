# Setting up Telegram Bot on HealthTools.KE-api
The Telegram Bot does the followinng:
1. Check to see if your doctor, nurse, or clinical officer is registered
2. Find out which facilities your NHIF card will cover in your county
3. Find the nearest doctor or health facility

### Installation
Make sure you have installed in your environment: `python-telegram-boy`

# Create a new telegram bot
- https://telegram.me/BotFather
- After you create your bot, save the token assigned.

# ngrok Configuration
- ngrok allows you to expose a web server running on your local machine to the interne
- Install Ngrok
    [link][https://ngrok.com/]
- Follow the instructions on: https://ngrok.com/docs#expose
    Note: The listening port you use, is the same one your app should listen on. E.g.
    $ ngrok http 5000

    In manage.py,

    if __name__ == '__main__':
        app.run(
            host="localhost", # Since ngrok is running locally
            port=5000, # the app listens on the same port as ngrok
        )

- Configuration
    See the nginx.config.template

# Nginx Configuration
- Install Nginx
    https://www.nginx.com/resources/admin-guide/installing-nginx-open-source/
    or
    for mac users: https://coderwall.com/p/dgwwuq/installing-nginx-in-mac-os-x-maverick-with-homebrew

- Configuration
    See the nginx.config.template

# Environment variables

You can set the required environment variables like so
```
export BOT_TOKEN=<telegram-bot-token-assigned-by-BotFather>

# Note: Telegram Bot only works with HTTPS
export BOT_WEBHOOK_URL=<https-forwarding-address-from-ngrok>
export SERVER_IP="localhost"
export TELEGRAM_PORT=5000

# openssl req -newkey rsa:2048 -sha256 -nodes -keyout private.key -x509 -days 3650 -out cert.pem
export CERT_FILE=</path/to/cert/file>
export KEY_FILE=</path/to/keu/file>
```
