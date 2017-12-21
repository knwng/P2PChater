import numpy as np
import socket
from config import *
from time import ctime
socket.setdefaulttimeout(TIMEOUT)

class Comm2Server(object):
    def __init__(self, dst_ip, dst_port, account, passwd='net2017'):
        self.server_address = (dst_ip, dst_port)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_sock.setblocking(False)
        # self.server_sock.settimeout(5)       # set timeout to 5s
        self.account = account
        self.passwd = passwd
        self.friend_list = []
        self.chatting_port = 12500      # port for receiving chatting request
        print('Socket name: ', self.server_sock.getsockname())

    def login(self):
        try:
            self.server_sock.connect(self.address)
        except socket.gaierror, e:
            print 'Address-related error connecting to server: {}'.format(e)
            return None
        except socket.error, e:
            print 'Connection Error: {}'.format(e)
            # self.server_sock.close()
            return None
        except socket.timeout, e:
            print 'Connection Timeout: {}'.format(e)
            return None
        try:
            self.server_sock.sendall('{}_{}'.format(self.account, self.passwd))
        except socket.error, e:
            print 'Error sending data: {}'.format(e)
            return None
        except socket.timeout, e:
            print 'Sending Timeout: {}'.format(e)
            return None
        try:
            reply = self.server_sock.recv(BUFFERSIZE)
        except socket.timeout, e:
            print 'Receiving Timeout: {}'.format(e)
            return None
        # print('reply: ', reply)
        return reply == 'lol'

    def logout(self):
        # self.server_sock.connect(self.address)
        self.server_sock.sendall('logout'+self.account)
        reply = self.server_sock.recv(BUFFERSIZE)
        # print('reply: ', reply)
        self.server_sock.close()
        return reply == 'loo'

    def query(self, faccount):
        # self.server_sock.connect(self.address)
        self.server_sock.sendall('q'+faccount)
        reply = self.server_sock.recv(BUFFERSIZE)
        print('reply: ', reply)
        # self.server_sock.close()
        if reply == 'n':
            return None
        return reply

    def get_friend_status(self):
        with file(friend_list_fn, 'r') as f:
            flt = f.readlines()
        for i in flt:
            self.friend_list.append(Friends(i, self.query(i)))

    def setup_listen_socket(self):
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_sock.bind((''. LISTENPORT))
        self.listen_sock.listen(10)

    def listen_chatting_request(self):
        # addr in format (ip, port)
        client_sock, addr = self.listen_sock.accept()
        # for i in self.friend_list:
        #     if i.ip == addr[0]:
        #         print('Receive chatting request from {} who is not a friend of mine'.format(addr))
        #         return None
        idx = None
        for i in range(len(self.friend_list)):
            if self.friend_list[i].ip == addr[0]:
                idx = i
                break
        if idx is None:
            print("Can't find ip: {} in friend_list".format(addr[0]))
            return False
        client_sock.settimeout(TIMEOUT)
        data = client_sock.recv(BUFFERSIZE)
        # data should in format: request_port
        if not data.startswith('request'):
            print('Invalid chatting request')
            return False
        self.friend_list[i].in_use = True
        self.friend_list[i].chat_client = CommP2P(addr[0], data.split('_')[1])
        return True

    def get_valid_port(self):
        s = socket.socket()
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port


class CommP2P(object):
    def __init__(self, dst_ip, dst_port):
        self.dst_port = dst_port
        self.address = (dst_ip, dst_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.src_port = self.sock.getsockname()[1]
        self.sock.connect(self.address)
        self.sock.setblocking(False)
        # msg in format (timestamps, msg, flag)
        # flag = 1 for user himself, 2 for his friend
        self.msg = []

    def send_msg(self, data):
        self.msg.append([ctime(), data, 1])
        self.sock.sendall(data)
        return

    def recv_msg(self):
        data = self.sock.recv(BUFFERSIZE)

        return

    def send_file(self, filename):
        pass

    def recv_file(self):
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
