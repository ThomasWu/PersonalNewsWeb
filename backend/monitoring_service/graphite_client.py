import os
import socket
import sys
import time

CARBON_URL = '0.0.0.0'
CARBON_PORT = 2003

def logPerformance(msg):
    sock = socket.socket()
    sock.connect((CARBON_URL, CARBON_PORT))
    sock.sendall(msg)
    sock.close()

    