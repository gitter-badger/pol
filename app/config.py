# config
import datetime
import os
from flask_peewee.db import Database

db_path = os.path.join(os.environ.get('HOME', os.environ.get('USERPROFILE')), 'db', 'www.trim21.cn.db')

sec = os.getenv('website_secret')
ppoi_secret = os.getenv('ppoi_key', '')

if not sec and ppoi_secret:
    print('mission sec or ppoi_secret')
    exit(1)

class Configuration(object):
    # DATABASE = {
    #     'name': db_path,
    #     'engine': 'peewee.SqliteDatabase',
    #     'check_same_thread': False,
    # }
    DEBUG = False
    TEMPLATES_AUTO_RELOAD = True

    SECRET_KEY = sec

    # flask-login
    REMEMBER_COOKIE_SECURE = True

    REMEMBER_COOKIE_DURATION = datetime.timedelta(minutes=30)


workload = 1024 * 2
if os.environ.get('DEV', False):
    workload = 256
