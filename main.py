# -*- coding: utf-8 -*-
from Backend import *
from config import *
import time



def main():
    client = Comm2Server('166.111.140.14', 8000, '2014010622')
    friend = Comm2Server('166.111.140.14', 8000, '2014011653')
    print ('Login: ', client.login())
    print ('Friend Login:', friend.login())
    # print ('Friend Login: ', friend.logout())
    print ('query: ', client.query('2014011653'))
    print ('query: ', client.query('2014010622'))
    print ('Logout: ', client.logout())
    # print ('Friend Logout: ', friend.logout())

if __name__ == '__main__':
    main()
