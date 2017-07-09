import json
import pika

class CloudAMQPClient:
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = 3
        # connects to CloudAMQP
        self.connection = pika.BlockingConnection(self.params)
        # starts a channel
        self.channel = self.connection.channel()
        # declares a queue
        self.channel.queue_declare(queue=queue_name)

    # sends a message
    def sendMessage(self, message):
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message)
        )
        # TODO: logs to log system

    # gets a message
    def getMessage(self):
        method_frame, header_frame, body = self.channel.basic_get(self.queue_name)
        if method_frame:
            self.channel.basic_ack(method_frame.delivery_tag)
            # TODO: logs to log system
            return json.loads(body)
        else:
            # TODO: logs to log system
            return None

    # BlockingConnection.sleep is a safer way to sleep than time.sleep(). This
    # will repond to server's heartbeat.
    def sleep(self, seconds):
        self.connection.sleep(seconds)