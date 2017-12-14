import numpy as np
import socket


class Comm2Server(object):
    def __init__(self, dst_ip, dst_port):
        # self.dst_ip = dst_ip
        # self.dst_port = dst_port
        self.address = (dst_ip, dst_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def comm(self, data):
        self.sock.connect(self.address)
        print('Socket name: ', self.sock.getsockname())
        self.sock.sendall(data)
        reply = rcvall(self.sock, 1024)
        self.sock.close()
        return reply


class CommP2P(object):
    def __init__(self):
        pass


def rcvall(sock, buffer_length):
    data = b''
    while len(data) < buffer_length:
        remain = sock.recv(buffer_length - len(data))
        if not remain:
            raise EOFError('buffer size is %d but only received %d '.format(buffer_length, len(data)))
        data += remain
    return data
