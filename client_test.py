import os,sys
import socket

BUFSIZE = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('localhost', 12500))

# sock.send('data from localhost')
sock.send('break')
data = sock.recv(BUFSIZE)
print('msg from server: {}'.format(data))

sock.close()
