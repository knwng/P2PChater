import re
BUFFERSIZE = 1024
LISTENPORT = 12500
TIMEOUT = 2
friend_list_fn = 'friend_list'
pattern_ip = re.compile(r'^([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.([1-9]?'
                        r'\d|1\d\d|2[0-4]\d|25[0-5])\.([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])$')
pattern_id = re.compile(r'^201[4-5]01[0-1]\d{3}')


class Friends:

    def __init__(self, name='', is_online=False, ip='', is_use=False, unread=0, chat_client=None):
        self.name = name
        self.is_online = is_online
        self.ip = ip
        self.is_use = is_use
        self.chat_client = chat_client
        self.unread = unread
        self.msg = []
        # msg in format [timestamp, id_identifier, msg]
        return

    def clear_connection_info(self):
        self.is_online = False
        self.ip = ''
        self.is_use = False
        self.unread = 0
        self.chat_client = None
        self.msg = []
        return

    def display(self):
        print('Name: {} | ip: {} | MSG: {}'.format(self.name, self.ip, self.msg))
        return
