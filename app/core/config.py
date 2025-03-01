import os
import secrets
from pathlib import Path
from urllib.parse import urlencode

import pytz

PROJ_ROOT = Path(os.path.join(os.path.dirname(__file__), '..'))

APP_NAME = 'trim21-www-server'

DEBUG = bool(os.getenv('DEBUG'))

DSN = os.getenv('DSN')

COMMIT_TAG = os.getenv('COMMIT_TAG')
COMMIT_SHA = (os.getenv('COMMIT_SHA') or 'None')[:8]

COMMIT_REV = COMMIT_TAG or COMMIT_SHA

TIMEZONE = pytz.timezone('Etc/GMT-8')

MYSQL_HOST = os.getenv('MYSQL_HOST')
MYSQL_USER = os.getenv('MYSQL_USER')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')
MYSQL_DB = os.getenv('MYSQL_DB')
DATABASE_URI = f'mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}'

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

REDIS_URI = f'redis://{REDIS_HOST}/0'

if REDIS_PASSWORD:
    REDIS_URI = f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}/0'

RABBITMQ_ADDR = os.getenv('RABBITMQ_ADDR')
RABBITMQ_USER = os.getenv('RABBITMQ_USER')
RABBITMQ_PASS = os.getenv('RABBITMQ_PASS')

VIRTUAL_HOST = os.environ.get('VIRTUAL_HOST', 'localhost:6001')
PROTOCOL = os.environ.get('PROTOCOL', 'http')

SECRET_KEY = (os.getenv('SECRET_KEY') or secrets.token_hex(32))[:32]
assert len(SECRET_KEY) == 32


class BgmTvAutoTracker:
    APP_ID = os.environ.get('BGM_TV_AUTO_TRACKER_APP_ID')
    APP_SECRET = os.environ.get('BGM_TV_AUTO_TRACKER_APP_SECRET')
    callback_url = (
        f'{PROTOCOL}://{VIRTUAL_HOST}/bgm-tv-auto-tracker'
        f'/api.v1/oauth_callback'
    )
    oauth_url = 'https://bgm.tv/oauth/authorize?' + urlencode({
        'client_id': APP_ID,
        'response_type': 'code',
        'redirect_uri': callback_url,
    })
