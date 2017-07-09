import mongodb_client as client

def test_basic():
    db = client.get_db(
        host='mongodb://ds025782.mlab.com', 
        port='25782', 
        db='news', 
        username='admin',
        password='123456')
    db.test.drop()
    assert db.test.count() == 0
    db.test.insert({'test': 1})
    assert db.test.count() == 1
    db.test.drop()
    assert db.test.count() == 0
    print 'test_basic passed'

if __name__ == '__main__':
    test_basic()
