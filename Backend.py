import numpy as np
import socket
from config import *


class Comm2Server(object):
    def __init__(self, dst_ip, dst_port, account, passwd='net2017'):
        # self.dst_ip = dst_ip
        # self.dst_port = dst_port
        self.address = (dst_ip, dst_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.account = account
        self.passwd = passwd
        self.sock.connect(self.address)
        self.friend_list = {}
        print('Socket name: ', self.sock.getsockname())

    def login(self):
        self.sock.sendall('{}_{}'.format(self.account, self.passwd))
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

    def get_friend_status(self):
        with file(friend_list_fn, 'r') as f:
            flt = f.readlines()
        for i in flt:
            self.friend_list[i] = self.query(i)

    def chat(self, friend):
        if friend not in self.friend_list.keys():
            return None
        if self.friend_list[friend] is None:
            return None

        return CommP2P(self.friend_list[friend], 8000)


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
