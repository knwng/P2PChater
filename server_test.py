#!/usr/bin/env/ python2
import os,sys
import socket

BUFSIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
localhost = '127.0.0.1'
sock.bind((localhost, 12500))
sock.listen(10)

print('Server socket: {}'.format(sock.getsockname()))

while True:
    conn, addr = sock.accept()
    print('Connected by: {}'.format(addr))
    
    while True:
        data = conn.recv(BUFSIZE)
        if not data:
            break
        if data.endswith('break'):
            print('get msg to quit')
            sock.close()
            sys.exit()
        print('Received msg: {}'.format(data))
        conn.send('Received your data')
    conn.close()
sock.close()

