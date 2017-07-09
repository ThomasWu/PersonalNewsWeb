from pymongo import MongoClient

def get_db(host, port, db, username=None, password=None):
    client = MongoClient('%s:%s' % (host, port))
    db = client[db]
    if username is not None and password is not None:
        db.authenticate(username, password)
    return db