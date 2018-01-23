# install_twisted_rector must be called before importing and using the reactor
from kivy.support import install_twisted_reactor

install_twisted_reactor()

from twisted.internet import reactor
from twisted.internet import protocol


class EchoServer(protocol.DatagramProtocol):

    def __init__(self, app):
        # super(EchoServer, self).__init__()
        self.app = app

    def datagramReceived(self, data, address):
        print('Receive message [{}] from [{}]'.format(data, address))
        response = self.app.handle_message(data)
        response = 'MSG_2014011653_'+data[15:]
        if response:
            self.transport.write(response, ('127.0.0.1', 12500))


class EchoServerFactory(protocol.Factory):
    protocol = EchoServer

    def __init__(self, app):
        self.app = app


from kivy.app import App
from kivy.uix.label import Label


class TwistedServerApp(App):
    label = None

    def build(self):
        self.label = Label(text="server started\n")
        reactor.listenUDP(8000, EchoServer(self))
        return self.label

    def handle_message(self, msg):
        msg = msg.decode('utf-8')
        self.label.text = "received:  {}\n".format(msg)

        if msg == "ping":
            msg = "Pong"
        if msg == "plop":
            msg = "Kivy Rocks!!!"
        self.label.text += "responded: {}\n".format(msg)
        return msg.encode('utf-8')


if __name__ == '__main__':
    TwistedServerApp().run()