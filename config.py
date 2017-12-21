
BUFFERSIZE = 1024
LISTENPORT = 12500
TIMEOUT = 2
friend_list_fn = 'friend_list'


class Friends(object):
    def __init__(self, name='', ip='', in_use=False, chat_client=None):
        self.name = name
        self.ip = ip
        self.in_use = in_use
        self.chat_client = chat_client

    def clear_connection_info(self):
        self.ip = None
        self.in_use = False
        self.chat_client = None

