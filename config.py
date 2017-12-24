import re
BUFFERSIZE = 1024
LISTENPORT = 12500
TIMEOUT = 2
friend_list_fn = 'friend_list'
pattern_ip = re.compile(r'^([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])$')
pattern_id = re.compile(r'^201[4-5]01[0-1]\d{3}')

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

