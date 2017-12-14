import numpy as np
import socket
from config import *


class Comm2Server(object):
    def __init__(self, dst_ip, dst_port, account):
        # self.dst_ip = dst_ip
        # self.dst_port = dst_port
        self.address = (dst_ip, dst_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.account = account
        self.sock.connect(self.address)
        print('Socket name: ', self.sock.getsockname())

    def login(self):
        self.sock.sendall(self.account+'_net2017')
        reply = self.sock.recv(BUFFERSIZE)
        # print('reply: ', reply)
        # self.sock.close()
        return reply == 'lol'

    def logout(self):
        # self.sock.connect(self.address)
        self.sock.sendall('logout'+self.account)
        reply = self.sock.recv(BUFFERSIZE)
        # print('reply: ', reply)
        self.sock.close()
        return reply == 'loo'

    def query(self, faccount):
        # self.sock.connect(self.address)
        self.sock.sendall('q'+faccount)
        reply = self.sock.recv(BUFFERSIZE)
        print('reply: ', reply)
        # self.sock.close()
        if reply == 'n':
            return None
        return reply


class CommP2P(object):
    def __init__(self, dst_ip, dst_port):
        self.address = (dst_ip, dst_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(self.address)

    def sendText(self, data):
        self.sock.sendall(data)
        return

    def rcvText(self):
        return self.sock.recv(BUFFERSIZE)

    def sendFile(self, filename):
        pass


'''
def rcvall(sock, buffer_length):
    data = b''
    while len(data) < buffer_length:
        remain = sock.recv(buffer_length - len(data))
        if not len(remain):
            break
            # raise EOFError('buffer size is %d but only received %d '.format(buffer_length, len(data)))
        data += remain
    return data
'''
