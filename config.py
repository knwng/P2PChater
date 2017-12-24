import re
BUFFERSIZE = 1024
LISTENPORT = 12500
TIMEOUT = 2
friend_list_fn = 'friend_list'
pattern_ip = re.compile(r'^([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])$')
pattern_id = re.compile(r'^201[4-5]01[0-1]\d{3}')

class Friends(object):
    def __init__(self, name='', is_online=False, ip='', is_use=False, chat_client=None, in_msg=[], out_msg=[]):
        self.name = name
        self.is_online = is_online
        self.ip = ip
        self.is_use = is_use
        self.chat_client = chat_client
        self.in_msg = in_msg
        self.out_msg = out_msg

    def clear_connection_info(self):
        self.is_online = False
        self.ip = None
        self.in_use = False
        self.chat_client = None
