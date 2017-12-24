import numpy as np
from config import *
import socket
socket.setdefaulttimeout(TIMEOUT)
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from time import ctime
from kivy.clock import Clock
from kivy.uix.widget import Widget
from twisted.internet import reactor, protocol
import re


def esc_markup(msg):
    return (msg.replace('&', '&amp;')
            .replace('[', '&bl;')
            .replace(']', '&br;'))


class LoginClient(protocol.Protocol):
    def connectionMade(self):
        # send 'CONNECT' message and
        # force TCP flush by appending a line feed ('\n')
        # self.transport.write('CONNECT\n')
        self.factory.app.on_login_conn(self.transport)

    def dataReceived(self, data):
        # self.factory.app.on_message(data)
        print('Received data: {}'.format(data))
        if self.factory.app.login_status is False:
            if data == 'lol':
                self.factory.app.login_callback(True)
            else:
                self.factory.app.login_callback(False)
        else:
            if data == 'n':
                self.factory.app.proc_friend_list(False)
            elif re.match(pattern_ip, data):
                self.factory.app.proc_friend_list(True, data)
            else:
                print('False query {} for friend status'.format(data))

class LoginClientFactory(protocol.ClientFactory):
    protocol = LoginClient

    def __init__(self, app):
        self.app = app


class FriendlistClient(protocol.Protocol):
    def connectionMade(self):
        # send 'CONNECT' message and
        # force TCP flush by appending a line feed ('\n')
        # self.transport.write('CONNECT\n')
        self.factory.app.on_friendlist_conn(self.transport)

    def dataReceived(self, data):
        print('Receive data from friend: {}'.format(data))
        if data == 'n':
            print('get n')
            self.factory.app.proc_friend_list(False)
        elif re.match(pattern_ip, data):
            print('get ip: {}'.format(data))
            self.factory.app.proc_friend_list(True, data)
        else:
            print('False query {} for friend status'.format(data))


class FriendlistClientFactory(protocol.ClientFactory):
    protocol = FriendlistClient

    def __init__(self, app):
        self.app = app


class RequestServer(protocol.Protocol):
    def dataReceived(self, data):
        response = self.factory.app.handle_message(data)
        if response:
            self.transport.write(response)


class RequestServerFactory(protocol.Factory):
    protocol = RequestServer

    def __init__(self, app):
        self.app = app


class Comm2ServerWidget(Widget):
    def __init__(self, dst_ip, dst_port, account, passwd='net2017'):
        self.server_address = (dst_ip, dst_port)
        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.server_sock.setblocking(False)
        # self.server_sock.settimeout(5)       # set timeout to 5s
        self.account = account
        self.passwd = passwd
        self.friend_list = []
        self.chatting_port = 12500      # port for receiving chatting request
        Clock.schedual_interval(self.update_friend_status(), 1)
        Clock.schedual_interval(self.listen_chatting_request(), 0.1)
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

    def update_friend_status(self):
        for i in self.friend_list:
            i.ip = self.query(i.name)
        return

    def setup_listen_socket(self):
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_sock.bind((''. LISTENPORT))
        self.listen_sock.listen(10)

    def listen_chatting_request(self):
        # addr in format (ip, port)
        client_sock, addr = self.listen_sock.accept()
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
        # data should in format: request
        if not data.startswith('request'):
            print('Invalid chatting request')
            return False
        self.friend_list[i].in_use = True
        self.friend_list[i].chat_client = CommP2P(1, addr[0], int(float(addr[1])))
        return True

    def get_valid_port(self):
        s = socket.socket()
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port



class CommP2PWidget(Widget):
    def __init__(self, type, dst_ip=None, dst_port=None):
        # type = 0 for client, type = 1 for server
        self.type = type
        if self.type == 0:
            self.dst_port = dst_port
            self.address = (dst_ip, dst_port)
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.src_port = self.client_sock.getsockname()[1]
        self.client_sock.connect(self.address)
        self.client_sock.setblocking(False)
        # msg in format (timestamps, msg, flag)
        # flag = 1 for user himself, 2 for his friend
        self.msg = []

    def send_msg(self, data):
        self.msg.append([ctime(), data, 1])
        self.client_sock.sendall(data)
        return

    def recv_msg(self):
        data = self.sock.recv(BUFFERSIZE)
        self.msg.append(list(data).append(2))
        return

    def send_file(self, filename):
        pass

    def recv_file(self):
        pass


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
        Clock.schedual_interval(self.update_friend_status(), 1)
        Clock.schedual_interval(self.listen_chatting_request(), 0.1)
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

    def update_friend_status(self):
        for i in self.friend_list:
            i.ip = self.query(i.name)
        return

    def setup_listen_socket(self):
        self.listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_sock.bind((''. LISTENPORT))
        self.listen_sock.listen(10)

    def listen_chatting_request(self):
        # addr in format (ip, port)
        client_sock, addr = self.listen_sock.accept()
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
        # data should in format: request
        if not data.startswith('request'):
            print('Invalid chatting request')
            return False
        self.friend_list[i].in_use = True
        self.friend_list[i].chat_client = CommP2P(1, addr[0], int(float(addr[1])))
        return True

    def get_valid_port(self):
        s = socket.socket()
        s.bind(('', 0))
        port = s.getsockname()[1]
        s.close()
        return port


class CommP2P(object):
    def __init__(self, type, dst_ip=None, dst_port=None):
        # type = 0 for client, type = 1 for server
        self.type = type
        if self.type == 0:
            self.dst_port = dst_port
            self.address = (dst_ip, dst_port)
            self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.src_port = self.client_sock.getsockname()[1]
        self.client_sock.connect(self.address)
        self.client_sock.setblocking(False)
        # msg in format (timestamps, msg, flag)
        # flag = 1 for user himself, 2 for his friend
        self.msg = []

    def send_msg(self, data):
        self.msg.append([ctime(), data, 1])
        self.client_sock.sendall(data)
        return

    def recv_msg(self):
        data = self.sock.recv(BUFFERSIZE)
        self.msg.append(list(data).append(2))
        return

    def send_file(self, filename):
        pass

    def recv_file(self):
        pass

