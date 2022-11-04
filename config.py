# Configs
import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    DEBUG = True
    CACHE_TYPE = "SimpleCache"
    CACHE_DEFAULT_TIMEOUT = 300
    SQLALCHEMY_TRACK_MODIFICATIONS = False
