import os
import socket
import sys
import time
import graphite_client

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import configuration_service_client as conf_client
from cloudAMQP_client import CloudAMQPClient


MONITOR_TASK = 'graphite_monitor_task'
SLEEP_TIME_IN_SECONDS = 0.1

cloudAMQP_client = CloudAMQPClient(task=MONITOR_TASK)

def handle_message(msg):
    pass

def run():
    while True:
        if cloudAMQP_client is not None:
            msg = cloudAMQP_client.getMessage()
            if msg is not None:
                try:
                    handle_message(msg)
                except Exception as e:
                    print e
            cloudAMQP_client.sleep(SLEEP_TIME_IN_SECONDS)

if __name__ == '__main__':
    run()