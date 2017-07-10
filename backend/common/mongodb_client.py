from pymongo import MongoClient
import configuration_service_client as conf_client

SYSTEM_NAME = 'mongodb'

def get_db():
    # retrieves mongodb settings
    settings = conf_client.getSystemSettings(SYSTEM_NAME)
    client = MongoClient('%s:%s' % (settings['host'], settings['port']))
    db = client[settings['db']]
    # if 'username' in settings and 'password' in settings:
    db.authenticate(settings['username'], settings['password'])
    return db
