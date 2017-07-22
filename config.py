import os
from configparser import ConfigParser

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
DEBUG = False


def read_config():
    config = ConfigParser()
    config.read('secrets.ini')
    return config['main']

config_file = config_main = read_config()
access_password = config_main['secret']