from cloudAMQP_client import CloudAMQPClient

CLOUDAMQP_URL = 'amqp://qyvxxytd:q2jeUmNZFfO5ExqupNzrdc3u93fxS6J4@fish.rmq.cloudamqp.com/qyvxxytd'
QUEUE_NAME = 'test'


def test_basic():
    client = CloudAMQPClient(CLOUDAMQP_URL, QUEUE_NAME)
    sentMsg = {'test_key': 'test_value'}
    client.sendMessage(sentMsg)
    client.sleep(5)
    receivedMsg = client.getMessage()
    assert sentMsg == receivedMsg
    print 'test_basic passed'

if __name__ == '__main__':
    test_basic()