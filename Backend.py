from config import *
import socket
import time
import re
import os
socket.setdefaulttimeout(TIMEOUT)
from kivy.support import install_twisted_reactor
install_twisted_reactor()
from twisted.internet import reactor, protocol


def esc_markup(msg):
    return (msg.replace('&', '&amp;')
            .replace('[', '&bl;')
            .replace(']', '&br;'))


class LoginClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_login_conn(self.transport)

    def dataReceived(self, data):
        print('Received data from LoginClient: {}'.format(data))
        if self.factory.app.login_status is False:
            if data == 'lol':
                self.factory.app.login_callback(True)
            else:
                self.factory.app.userid = ''
                self.factory.app.login_callback(False)
        else:
            if data == 'loo':
                self.factory.app.logout_callback(True)
            else:
                self.factory.app.logout_callback(False)

class LoginClientFactory(protocol.ClientFactory):
    protocol = LoginClient

    def __init__(self, app):
        self.app = app


class FriendlistClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_friendlist_conn(self.transport)

    def dataReceived(self, data):
        if data == 'n':
            self.factory.app.proc_friend_list(False)
        elif re.match(pattern_ip, data):
            self.factory.app.proc_friend_list(True, data)
        else:
            print('False query {} for friend status'.format(data))


class FriendlistClientFactory(protocol.ClientFactory):
    protocol = FriendlistClient

    def __init__(self, app):
        self.app = app


class FileServer(protocol.Protocol):

    def dataReceived(self, data):
        # in format FILE_userid_data
        print('File Server received data: [{}]'.format(type(data)))
        if len(self.factory.filebuffer) == 0:
            if data.startswith('FILE'):
                userid = data.split('_')[1]
                if re.match(pattern_id, userid) is not None:
                    self.factory.sending_id = userid
                    self.factory.filebuffer += data[16:]
                else:
                    print("Got the head of file but userid {} is wrong".format(userid))
            else:
                print('The message is not startwith FILE')
        else:
            eof_idx = data.find('FILEEND')
            if eof_idx > 0:
                self.factory.filebuffer += data[:eof_idx]
                print('File receiving queue: {}'.format(self.factory.app.filerecv_flag))
                if self.factory.sending_id in [x[0] for x in self.factory.app.filerecv_flag]:
                    idx = [x[0] for x in self.factory.app.filerecv_flag].index(self.factory.sending_id)
                    filename = self.factory.app.filerecv_flag[idx][1]
                    if os.path.exists(os.path.join('./user', self.factory.sending_id)) is None:
                        os.system('mkdir -p {}'.format(os.path.join('./user', self.factory.sending_id)))
                    with open(os.path.join('./user', self.factory.sending_id, filename), 'wb') as f:
                        f.write(self.factory.filebuffer)
                else:
                    print('{} is not in friend list'.format(self.factory.sending_id))
                print('Finish transfer, delete buffer')
                self.factory.sending_id = ''
                self.factory.filebuffer = ''
            else:
                print('Not found EOF, still transfering')
                self.factory.filebuffer += data
                if data.startswith('FILE'):
                    print('Find another file while transfering, transfer crashed, delete buffer')
                    self.factory.sending_id = ''
                    self.factory.filebuffer = ''


class FileServerFactory(protocol.Factory):
    protocol = FileServer

    def __init__(self, app):
        self.app = app
        self.sending_id = ''
        self.filebuffer = ''


class FileClient(protocol.Protocol):
    def connectionMade(self):
        self.factory.app.on_file_conn(self.transport)

    def dataReceived(self, data):
        pass


class FileClientFactory(protocol.ClientFactory):
    protocol = FileClient

    def __init__(self, app):
        self.app = app


class ChatClient(protocol.DatagramProtocol):

    def __init__(self, app):
        self.app = app

    def startProtocol(self):
        self.app.on_chatclient_connection(self.transport)

    def datagramReceived(self, data, address):
        print('Receive message {}'.format(data))
        if data.startswith('MSG'):
            # receive a msg, in format MSG_userid_data
            userid = data.split('_')[1]
            if re.match(pattern_id, userid):
                # format check passed
                for idx, i in enumerate(self.app.friend_list):
                    if i.name == userid:
                        # [timestamp, 0, data] 0 for in-msg
                        self.app.friend_list[idx].msg.append([time.time(), 0, data[15:]])
                        i.unread += 1
                        self.app.update_chat_window()
                        return
        elif data.startswith('FILE'):
            # FILE Request or FILE ACK
            # in format FILE_userid_{REQUEST_filename, ACK}
            userid = data.split('_')[1]
            if re.match(pattern_id, userid):
                if data.split('_')[2] == 'REQUEST':
                    # REQUEST to send file
                    filename = data[24:]
                    self.app.show_dialog('file_request', userid, filename)
                    pass
                elif data.split('_')[2] == 'ACK':
                    # ACK to receive file, start transfer
                    # send file in format FILE_userid_data
                    # filesend_flag: [userid, filepath]
                    print('File Sending Queue: [{}]'.format(self.app.filesend_flag))
                    if userid in [x[0] for x in self.app.filesend_flag]:
                        idx = [x[0] for x in self.app.filesend_flag].index(userid)
                        filepath = self.app.filesend_flag[idx][1]
                        self.app.filesend_flag.remove(self.app.filesend_flag[idx])
                        for idx, i in enumerate(self.app.friend_list):
                            if userid == i.name and i.is_online:
                                i.display()
                                print('filepath: {}'.format(filepath))
                                with open(filepath[0], 'rb') as f:
                                    filedata = f.read()
                                    if self.app.file_conn:
                                        self.app.file_conn.write('FILE_{}_{}_FILEEND'.format(self.app.userid, filedata))
                                        self.app.friend_list[idx].msg.append([time.time(), 1, os.path.basename(filepath[0])])
                                        break
                                    else:
                                        print('file conn are lost')
                            else:
                                print('userid {} is wrong or is not online'.format(userid))
                    else:
                        print('{} are not in file sending queue'.format(userid))
                    pass
                elif data.split('_')[2] == 'REFUSE':
                    # your sending request are refused
                    self.app.file_conn.loseConnection()
                    del self.app.file_conn
                    self.app.show_dialog('refused')
                    pass
                else:
                    print('FILE type neither REQUEST nor ACK')
        return


class RequestServer(protocol.Protocol):

    def dataReceived(self, data):
        self.factory.app.handle_chat_request(data)


class RequestServerFactory(protocol.Factory):
    protocol = RequestServer

    def __init__(self, app):
        self.app = app
