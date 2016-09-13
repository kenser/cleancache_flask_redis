#-*-coding:utf8-*-
import os

#-- redis config --
REDIS_URL = "redis://localhost:6379/0"

#-- app config --
DEBUG = True
SECRET_KEY = "secret-key"
SESSION_COOKIE_NAME = "cache"
PERMANENT_SESSION_LIFETIME = 3600 * 24 * 30
SITE_COOKIE = "cache-ck"


PWD = os.getcwd()
LOG_PATH = os.path.join(PWD,"logs/")
LOG_NAME = "clear_caches.log"

