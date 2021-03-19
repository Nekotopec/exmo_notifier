import os

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

if not TELEGRAM_TOKEN:
    raise TypeError('TELEGRAM TOKEN can`t be blank.\n'
                    '   Set environment var `TELEGRAM_TOKEN` with your token.')


# List of chat ids.
CHAT_IDS = [243279187]

# webhook settings
WEBHOOK_HOST = os.getenv('HOST')
WEBHOOK_PATH = f'/bot{TELEGRAM_TOKEN}/webhook'

# webhook self signed serts.
WEBHOOK_SSL_CERT = '../keys/url_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = '../keys/url_private.key'  # Path to the ssl private key

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBHOOK_PORT = 8443

WEBHOOK_URL = f"https://{WEBHOOK_HOST}:{WEBHOOK_PORT}{WEBHOOK_PATH}"