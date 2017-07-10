import os
import socket
import sys
import time
import graphite_client

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'common'))
import configuration_service_client as conf_client
from cloudAMQP_client import CloudAMQPClient



def handle_message(msg):
    pass

def run():
    while True:
        pass


if __name__ == '__main__':
    run()