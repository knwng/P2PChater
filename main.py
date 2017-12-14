from Backend import *


def main():
    client = Comm2Server('166.111.140.14', 8000)
    # reply = client.comm(b'2014010622_net2017')
    reply = client.comm(b'2015010173_net2017')
    print(reply)


if __name__ == '__main__':
    main()
