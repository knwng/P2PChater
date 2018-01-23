# install_twisted_rector must be called before importing the reactor
from __future__ import unicode_literals

from kivy.support import install_twisted_reactor

install_twisted_reactor()

# A Simple Client that send messages to the Echo Server
from twisted.internet import reactor, protocol


class EchoClient(protocol.DatagramProtocol):

    def __init__(self, app):
        # super(EchoClient, self).__init__()
        print('app instance {}'.format(app))
        self.app = app
        # self.app.on_connection(self.transport)

    def startProtocol(self):
        # self.transport.connect('127.0.0.1', 8000)
        self.app.on_connection(self.transport)

    def datagramReceived(self, data, address):
        print('Receive message [{}] from [{}]'.format(data, address))
        # self.factory.app.print_message(data.decode('utf-8'))


class EchoClientFactory(protocol.ClientFactory):
    protocol = EchoClient

    def __init__(self, app):
        self.app = app
    #
    # def startedConnecting(self, connector):
    #     self.app.print_message('Started to connect.')
    #
    # def clientConnectionLost(self, connector, reason):
    #     self.app.print_message('Lost connection.')
    #
    # def clientConnectionFailed(self, connector, reason):
    #     self.app.print_message('Connection failed.')


from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout


# A simple kivy App, with a textbox to enter messages, and
# a large label to display all the messages received from
# the server
class TwistedClientApp(App):
    connection = None
    textbox = None
    label = None

    def build(self):
        root = self.setup_gui()
        self.connect_to_server()
        return root

    def setup_gui(self):
        self.textbox = TextInput(size_hint_y=.1, multiline=False)
        self.textbox.bind(on_text_validate=self.send_message)
        self.label = Label(text='connecting...\n')
        layout = BoxLayout(orientation='vertical')
        layout.add_widget(self.label)
        layout.add_widget(self.textbox)
        return layout

    def connect_to_server(self):
        # reactor.listenUDP(8001, EchoClient(self))
        reactor.listenUDP(8000, EchoClient(self))

    def on_connection(self, connection):
        self.print_message("Instance [{}] Connected successfully!".format(connection))
        self.connection = connection

    def send_message(self, *args):
        msg = self.textbox.text
        print('Conn instance is [{}]'.format(self.connection))
        print('msg is [{}]'.format(msg))
        if msg and self.connection:
            self.connection.write(msg.encode('utf-8'), ('127.0.0.1', 12500))
            # self.connection.write(msg.encode('utf-8'))
            self.textbox.text = ""

    def print_message(self, msg):
        self.label.text += "{}\n".format(msg)


if __name__ == '__main__':
    TwistedClientApp().run()