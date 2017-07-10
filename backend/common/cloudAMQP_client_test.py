from cloudAMQP_client import CloudAMQPClient

QUEUE_NAME = 'test'

def test_basic():
    client = CloudAMQPClient(queue_name=QUEUE_NAME)
    sentMsg = {'test_key': 'test_value'}
    client.sendMessage(sentMsg)
    client.sleep(5)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print 'test_basic passed'

if __name__ == '__main__':
    test_basic()