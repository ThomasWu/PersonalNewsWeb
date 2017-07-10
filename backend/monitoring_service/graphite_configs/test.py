import socket
import time
import psutil

CARBON_URL = '0.0.0.0'
CARBON_PORT = 2003

def sendToMatrix(msg):
    sock = socket.socket()
    sock.connect((CARBON_URL, CARBON_PORT))
    sock.sendall(msg)
    sock.close()

while True:
    timestamp = int(time.time())
    msgs = [
        'system.cpu %f %d' % (psutil.cpu_percent(), timestamp),
        'system.memory.free %d %d' % (psutil.virtual_memory().free, timestamp)
    ]
    print '\n'.join(msgs)
    sendToMatrix('\n'.join(msgs) + '\n')
    time.sleep(10)
