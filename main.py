# -*- coding: utf-8 -*-
from Backend import *
from config import *
from ui import *
import os, sys, time
from os.path import sep, expanduser, dirname
from numpy import argsort

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.utils import get_color_from_hex

from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import OneLineListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker
from kivymd.color_definitions import colors
from kivymd.textfields import MDTextField
from garden.filebrowser import FileBrowser


main_widget_kv = '''
#:import Toolbar kivymd.toolbar.Toolbar
#:import ThemeManager kivymd.theming.ThemeManager
#:import MDNavigationDrawer kivymd.navigationdrawer.MDNavigationDrawer
#:import NavigationLayout kivymd.navigationdrawer.NavigationLayout
#:import NavigationDrawerDivider kivymd.navigationdrawer.NavigationDrawerDivider
#:import NavigationDrawerToolbar kivymd.navigationdrawer.NavigationDrawerToolbar
#:import NavigationDrawerSubheader kivymd.navigationdrawer.NavigationDrawerSubheader
#:import MDCheckbox kivymd.selectioncontrols.MDCheckbox
#:import MDSwitch kivymd.selectioncontrols.MDSwitch
#:import MDList kivymd.list.MDList
#:import OneLineListItem kivymd.list.OneLineListItem
#:import TwoLineListItem kivymd.list.TwoLineListItem
#:import ThreeLineListItem kivymd.list.ThreeLineListItem
#:import OneLineAvatarListItem kivymd.list.OneLineAvatarListItem
#:import OneLineIconListItem kivymd.list.OneLineIconListItem
#:import OneLineAvatarIconListItem kivymd.list.OneLineAvatarIconListItem
#:import MDTextField kivymd.textfields.MDTextField
#:import MDSpinner kivymd.spinner.MDSpinner
#:import MDCard kivymd.card.MDCard
#:import MDSeparator kivymd.card.MDSeparator
#:import MDDropdownMenu kivymd.menu.MDDropdownMenu
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import colors kivymd.color_definitions.colors
#:import SmartTile kivymd.grid.SmartTile
#:import MDSlider kivymd.slider.MDSlider
#:import MDTabbedPanel kivymd.tabs.MDTabbedPanel
#:import MDTab kivymd.tabs.MDTab
#:import MDProgressBar kivymd.progressbar.MDProgressBar
#:import MDAccordion kivymd.accordion.MDAccordion
#:import MDAccordionItem kivymd.accordion.MDAccordionItem
#:import MDAccordionSubItem kivymd.accordion.MDAccordionSubItem
#:import MDThemePicker kivymd.theme_picker.MDThemePicker
#:import MDBottomNavigation kivymd.tabs.MDBottomNavigation
#:import MDBottomNavigationItem kivymd.tabs.MDBottomNavigationItem
#:import QRCodeWidget kivy.garden.qrcode

BoxLayout:
    orientation: 'vertical'
    ScreenManager:
        id: scr_mngr
        Screen:
            name: 'login'
            # id: login
            ScrollView:
                FloatLayout:
                    # orientation: 'vertical'
                    # size_hint_y: None
                    # height: self.minimum_height
                    # width: self.minimum_width
                    # padding: dp(48)
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    spacing: 20
                    MDTextField:
                        id: username
                        hint_text: "Username"
                        required: True
                        multiline: False
                        color_mode: 'accent'
                        helper_text: "Student ID"
                        helper_text_mode: "on_focus"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
                        size_hint: 0.5, 0.1
                    MDTextField:
                        id: password
                        hint_text: "Password"
                        required: True
                        multiline: False
                        color_mode: 'accent'
                        helper_text: "net2017"
                        password: True
                        helper_text_mode: "on_focus"
                        pos_hint: {'center_x': 0.5, 'center_y': 0.55}
                        size_hint: 0.5, 0.1
                    MDRaisedButton:
                        text: "Login"
                        pos_hint:{'right': 0.35, 'center_y': 0.45}
                        on_release: app.get_username_passwd()
                        size_hint: 0.1, 0.05
        Screen:
            name: 'mainpage'
            MDBottomNavigation:
                id: main_navigation
                MDBottomNavigationItem:
                    name: 'Chat'
                    text: "Chat"
                    icon: "alert-octagon"
                    id: chat
                    ScrollView:
                        do_scroll_x: False
                        MDList:
                            id: ml
                MDBottomNavigationItem:
                    name: 'Moment'
                    text: "Moment"
                    icon: 'bank'
                    id: moment
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        padding: dp(48)
                        spacing: 10
                        MDLabel:
                            font_style: 'Headline'
                            theme_text_color: 'Primary'
                            text: "Coming Soon"
                            # pos_hint: {'center_x': 0.7, 'center_y': 0.6}
                            # size_hint: 0.6, 0.4
                            halign: 'center'
                MDBottomNavigationItem:
                    name: 'Profile'
                    text: "Profile"
                    icon: 'alert'
                    id: profile
                    FloatLayout:
                        orientation: 'vertical'
                        # size_hint: 1, 1
                        FloatLayout:
                            orientation: 'vertical'
                            # size_hint: 1, 0.4
                            # pos_hint: {'center_x': 0.5, 'center_y': 0.8}
                            QRCodeWidget:
                                id: qr
                                data: ''
                                pos_hint: {'center_x': 0.3, 'center_y': 0.6}
                                size_hint: 0.4, 0.4
                                show_border: False
                            MDLabel:
                                font_style: 'Headline'
                                theme_text_color: 'Primary'
                                text: "Make Friend with Me!"
                                pos_hint: {'center_x': 0.7, 'center_y': 0.6}
                                size_hint: 0.6, 0.4
                                halign: 'center'
                        FloatLayout:
                            orientation: 'horizontal'
                            size_hint: 1, 0.3
                            pos_hint: {'center_x': 0.5, 'bottom': 0}
                            MDRaisedButton:
                                size: 3 * dp(48), dp(48)
                                # center_x: self.parent.center_x
                                text: 'Add Friend'
                                # opposite_colors: True
                                pos_hint: {'center_x': 0.3, 'center_y': 0.5}
                                on_release: app.add_friend()
                            MDRaisedButton:
                                size: 3 * dp(48), dp(48)
                                text: 'Change theme'
                                on_release: MDThemePicker().open()
                                opposite_colors: True
                                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                            MDRaisedButton:
                                size: 3 * dp(48), dp(48)
                                # center_x: self.parent.center_x
                                text: 'Logout'
                                opposite_colors: True
                                md_bg_color: get_color_from_hex(colors['Red']['500'])
                                pos_hint: {'center_x': 0.7, 'center_y': 0.5}
                                on_release: app.logout()
        Screen:
            name: 'chatroom'
            FloatLayout:
                # size_hint: None, None
                size: 1, 1
                orientation: 'vertical'
                Toolbar:
                    id: chatroom_toolbar
                    title: 'ChatRoom'
                    pos_hint: {'center_x': 0.5, 'top': 1}
                    # top: 1
                    # left: 0
                    size_hint: 1, 0.1
                    width: self.parent.width
                    # size_hint_min_x: 100
                    # size_hint_max_y: 0.2
                    # md_bg_color: get_color_from_hex(colors['DeepPurple']['A400'])
                    # background_palette: 'DeepPurple'
                    # background_hue: 'A400'
                    md_bg_color: get_color_from_hex(colors['Blue']['200'])
                    left_action_items: [['arrow-left', lambda x: app.back_to_mainpage()]]
                BoxLayout:
                    orientation: 'vertical'
                    pos_hint: {'center_x': 0.5, 'top': 0.9}
                    # size_hint: 1, 0.7
                    # size_hint: None, None
                    ScrollView:
                        do_scroll_x: False
                        FloatLayout:
                            orientation: 'vertical'
                            id: chatroom_msg
                            size_hint: None, None
                            height: dp(3000)
                            width: dp(self.parent.width)
                            pos_hint: {'center_x': 0.5}
                FloatLayout:
                    orientation: 'horizontal'
                    pos_hint: {'left': 0, 'bottom': 0}
                    size_hint: 1, 0.1
                    MDIconButton:
                        icon: 'file'
                        pos_hint: {'left': 0.3, 'center_y': 0.5}
                        # disabled: disable_the_buttons.active
                        on_release: app.send_file()
                    MDTextField:
                        id: chatroom_input
                        required: True
                        multiline: True
                        color_mode: 'accent'
                        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                        size_hint: 0.6, 0.9
                        on_text_validate: app.send_msg()
                    MDRaisedButton:
                        text: "Send"
                        elevation_normal: 2
                        opposite_colors: True
                        pos_hint: {'right': 0.96, 'center_y': 0.5}
                        size_hint: 0.1, 0.4
                        md_bg_color: get_color_from_hex(colors['Blue']['200'])
                        on_release: app.send_msg()

        Screen:
            name: 'filebrowser'
            id: filebrowser
                                       
'''


class IRC(App):
    userid = ''
    error_dialog = None
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "P2PChater"
    msg = StringProperty('')
    login_conn = None
    friendlist_conn = None
    chat_conn = None
    file_conn = None
    friend_list = None
    curr_proc_friend = None
    login_status = False
    host = '166.111.140.14'
    server_port = 8000
    msg_port = 12500
    file_port = 12600
    widget_shape = None
    # [0] for userid
    # [1] for filename
    filerecv_flag = []
    # [0] for userid
    # [1] for filepath
    filesend_flag = []
    pwd = ''
    friend_list_fn = ''

    # parameters for test
    test_listen_port1 = 8000
    test_write_port1 = 8100
    test_listen_port2 = 8100
    test_write_port2 = 8000
    test_file_listen_port1 = 8200
    test_file_listen_port2 = 8300
    test_file_write_port1 = 8300
    test_file_write_port2 = 8200
    test_agent = 2  # in [1, 2]

    menu_items = [
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
        {'viewclass': 'MDMenuItem',
         'text': 'Example item'},
    ]

    def build(self):
        main_widget = Builder.load_string(main_widget_kv)
        self.bottom_navigation_remove_mobile(main_widget)

        self.comm2server(self.host, self.server_port)
        self.comm2friendlist(self.host, self.server_port)
        if self.test_agent == 1:
            reactor.listenUDP(self.test_listen_port1, ChatClient(self))
            reactor.listenTCP(self.test_file_listen_port1, FileServerFactory(self))
        else:
            reactor.listenUDP(self.test_listen_port2, ChatClient(self))
            reactor.listenTCP(self.test_file_listen_port2, FileServerFactory(self))
        return main_widget

    # Network

    def login(self, username, password, *args):
        if self.login_conn:
            self.login_conn.write('{}_{}'.format(username, password).encode('utf-8'))
        else:
            self.show_dialog('connection')
        return

    def login_callback(self, FLAG):
        if FLAG:
            self.login_status = True
            self.root.ids.qr.data = self.userid
            self.root.ids.scr_mngr.current = 'mainpage'
            self.get_friendlist()
            Clock.schedule_interval(self.get_friendlist, 1)
            print("Current login account: {}".format(self.userid))
        else:
            self.show_dialog('connection')

    def logout(self):
        self.login_conn.write('logout{}'.format(self.userid))
        pass

    def logout_callback(self, FLAG):
        if FLAG:
            self.root.ids.username.text = ''
            self.root.ids.password.text = ''
            self.login_status = False
            self.root.ids.scr_mngr.current = 'login'
            self.userid = ''
            self.friend_list_fn = ''

        else:
            self.show_dialog('logout')

    def add_friend(self):

        pass

    def get_friendlist(self, *args):
        if self.friend_list is None:
            if not os.path.exists(os.path.join('./user', self.userid)):
                os.system('mkdir -p {}'.format(os.path.join('./user', self.userid)))
            if not os.path.exists(os.path.join('./user', self.userid, 'friend_list')):
                os.system('touch {}'.format(os.path.join('./user', self.userid, 'friend_list')))
            self.friend_list_fn = os.path.join('./user', self.userid, 'friend_list')
            with file(self.friend_list_fn, 'r') as f:
                flt = f.readlines()
            flt = [x[0:-1] for x in flt if re.match(pattern_id, x) is not None]
            self.friend_list = []
            for i in flt:
                self.friend_list.append(Friends(name=i))
        self.curr_proc_friend = 0
        if len(self.friend_list) > 0:
            self.friendlist_conn.write('q{}'.format(self.friend_list[0].name))

    def query_friend(self, id):
        self.friendlist_conn.write(id.encode('utf-8'))
        self.friendlist_conn.loseConnection()
        return

    def proc_friend_list(self, flag, msg=None):
        self.friend_list[self.curr_proc_friend].is_online = flag
        if flag:
            self.friend_list[self.curr_proc_friend].ip = msg
        else:
            if self.friend_list[self.curr_proc_friend].is_online is True:
                # your friend disconnect from you
                self.chat_disconnect(self.curr_proc_friend)
        self.curr_proc_friend += 1
        if self.curr_proc_friend < len(self.friend_list):
            self.friendlist_conn.write('q{}'.format(self.friend_list[self.curr_proc_friend].name))
        else:
            self.show_friend_card()
        return

    def chat_disconnect(self, idx):
        # save log
        with open('log_{}'.format(self.friend_list[idx].name), 'a') as f:
            f.writelines(self.friend_list[idx].msg)
        self.friend_list[idx].clear_connection_info()

    def back_to_mainpage(self, *args):
        self.root.ids.scr_mngr.current = 'mainpage'
        return

    def update_chat_window(self, *args):
        if self.root.ids.scr_mngr.current == 'chatroom':
            userid = self.root.ids.chatroom_toolbar.title.split(' ')[2]
            for idx, i in enumerate(self.friend_list):
                if i.name == userid:
                    self.show_chat_window(idx)

    def show_friend_card(self):
        self.root.ids.ml.clear_widgets()
        for i in self.friend_list:
            if i.is_online:
                listwidget = OneLineListItem(text=i.name,
                                             theme_text_color='Custom',
                                             text_color=get_color_from_hex(colors['Amber']['700']),
                                             on_release=self.chatwith)
                iconwidget = IconLeftSampleWidget(icon='account')
                self.root.ids.ml.add_widget(listwidget)
            else:
                listwidget = OneLineListItem(text=i.name,
                                             theme_text_color='Custom',
                                             on_release=self.chatwith)
                iconwidget = IconLeftSampleWidget(icon='account-off')
                self.root.ids.ml.add_widget(listwidget)
        return

    def chatwith(self, instance):
        print('Widget {} are pressed'.format(instance.text))
        for i in range(len(self.friend_list)):
            if self.friend_list[i].name == instance.text:
                if self.friend_list[i].is_online is False:
                    self.show_dialog('offline')
                    return
                self.show_chat_window(i)
                return

    def show_chat_window(self, idx):
        self.root.ids.chatroom_toolbar.title = 'Chat With {}'.format(self.friend_list[idx].name)
        self.root.ids.chatroom_msg.clear_widgets()
        # sort msg by timestamp
        print('MSG from {}: {}'.format(self.friend_list[idx].name, self.friend_list[idx].msg))
        sorted_idx = argsort([x[0] for x in self.friend_list[idx].msg])
        total_msg = len(self.friend_list[idx].msg)
        num = 0
        # parent_shape in [width, height]
        parent_shape = [self.root.ids.scr_mngr.width, 100+100*total_msg]
        print('parent shape: {}'.format(parent_shape))
        self.root.ids.chatroom_msg.height = parent_shape[1]
        for i in sorted_idx:
            if self.friend_list[idx].msg[i][1] == 0:
                # income message
                self.root.ids.chatroom_msg.add_widget(MessageCard('left',
                                                                  self.friend_list[idx].name,
                                                                  self.friend_list[idx].msg[i][2],
                                                                  num,
                                                                  parent_shape).get_card())
            else:
                # output message
                self.root.ids.chatroom_msg.add_widget(MessageCard('right',
                                                                  self.friend_list[idx].name,
                                                                  self.friend_list[idx].msg[i][2],
                                                                  num,
                                                                  parent_shape).get_card())
            num += 1
        self.root.ids.scr_mngr.current = 'chatroom'
        return

    def send_msg(self):
        if self.root.ids.chatroom_input.text is None:
            return
        client_name = self.root.ids.chatroom_toolbar.title.split(' ')[-1]
        for idx, i in enumerate(self.friend_list):
            if i.name == client_name:
                msg = self.root.ids.chatroom_input.text
                # 0 for in-msg, 1 for out-msg
                self.friend_list[idx].msg.append([time.time(), 1, msg])
                if self.chat_conn is not None:
                    if self.test_agent == 1:
                        self.chat_conn.write('{}_{}_{}'.format('MSG', self.userid, msg), ('127.0.0.1', self.test_write_port1))
                    else:
                        self.chat_conn.write('{}_{}_{}'.format('MSG', self.userid, msg), ('127.0.0.1', self.test_write_port2))
                    self.root.ids.chatroom_input.text = ''
                    if self.root.ids.scr_mngr.current == 'chatroom':
                        self.show_chat_window(idx)
                else:
                    print('UDP Client Not setup, cannot chat')
                return

    def send_file(self):
        client_name = self.root.ids.chatroom_toolbar.title.split(' ')[-1]
        if sys.platform == 'win':
            user_path = dirname(expanduser('~')) + sep + 'Documents'
        else:
            user_path = expanduser('~') + sep + 'Documents'

        browser = FileBrowser(select_string='Select',
                              favorites=[(user_path, 'Documents')])
        browser.bind(
                on_success=lambda x: self._fbrowser_success(browser, client_name),
                on_canceled=lambda x: self._fbrowser_canceled(browser))
        self.root.ids.filebrowser.add_widget(browser)
        self.root.ids.scr_mngr.current = 'filebrowser'
        return

    def _fbrowser_canceled(self, instance):
        self.root.ids.scr_mngr.current = 'chatroom'
        print 'cancelled, Close self.'

    def _fbrowser_success(self, instance, client_name):
        print('Send file {} to {}'.format(instance.selection, client_name))
        self.root.ids.scr_mngr.current = 'chatroom'
        self.filesend_flag.append([client_name, instance.selection])
        for idx, i in enumerate(self.friend_list):
            i.display()
            if i.name == client_name and i.is_online:
                self.chat_conn.write('FILE_{}_REQUEST_{}'.format(self.userid,
                                                                 os.path.basename(instance.selection[0])),
                                     ('127.0.0.1', self.test_write_port1 if self.test_agent == 1 else self.test_write_port2))
                if self.test_agent == 1:
                    reactor.connectTCP(i.ip, self.test_file_write_port1, FileClientFactory(self))
                else:
                    reactor.connectTCP(i.ip, self.test_file_write_port2, FileClientFactory(self))
                break
        # Send Request

    def get_username_passwd(self):
        username = self.root.ids.username.text
        password = self.root.ids.password.text
        if password == 'net2017':
            if re.match(pattern_id, username):
                self.userid = username
                self.login(username, password)
        else:
            self.show_dialog('login')

    # connection_wrapper
    def comm2server(self, dst_host, dst_port):
        reactor.connectTCP(dst_host, dst_port, LoginClientFactory(self))
        return

    def comm2friendlist(self, dst_host, dst_port):
        reactor.connectTCP(dst_host, dst_port, FriendlistClientFactory(self))
        return

    # connection handle
    def on_login_conn(self, conn):
        self.login_conn = conn

    def on_friendlist_conn(self, conn):
        self.friendlist_conn = conn

    def on_chatclient_connection(self, conn):
        self.chat_conn = conn

    def on_file_conn(self, conn):
        self.file_conn = conn

    # dialogs
    def show_dialog(self, dialog_type, userid='', filename=''):
        """
        :param dialog_type: offline, login, connection, file_request, refused, logout, add_friend
        :return: None
        """
        if dialog_type == 'offline':
            label_text = 'This friend is currently offline'
            dialog_text = 'Friend is offline'
        elif dialog_type == 'login':
            label_text = 'Please Check your username and password'
            dialog_text = 'Wrong username/password!'
        elif dialog_type == 'connection':
            label_text = 'Please Check your Internet Connection'
            dialog_text = 'Connection Failed'
        elif dialog_type == 'file_request':
            label_text = 'Your Friend {} want to send file {} to you, do you want to accept?'.format(userid, filename)
            dialog_text = 'Sending File Request'
        elif dialog_type == 'refused':
            label_text = 'Your request to send file are refused'
            dialog_text = 'Request Refused'
        elif dialog_type == 'logout':
            label_text = 'Cannot connect to server, logout failed'
            dialog_text = 'Logout Error'
        elif dialog_type == 'add_friend':
            label_text = ''
            dialog_text = "Please Input your friend's userid"
        else:
            raise Exception, 'No such dialog_type'
        if dialog_type == 'add_friend':
            content = MDTextField(id='friend_name',
                                  hint_text='friend name',
                                  required=True,
                                  color_mode='accent',
                                  helper_text='your friend userid',
                                  helper_text_mode='on_focus')
        else:
            content = MDLabel(font_style='Body1',
                              theme_text_color='Secondary',
                              text=label_text,
                              size_hint_y=None,
                              valign='top')
            content.bind(texture_size=content.setter('size'))
        self.error_dialog = MDDialog(title=dialog_text,
                                     content=content,
                                     size_hint=(.8, None),
                                     height=dp(200),
                                     auto_dismiss=False)
        self.error_dialog.add_action_button("OK",
                                            action=lambda *x: self.dialog_dismiss(dialog_type,
                                                                                        userid,
                                                                                        filename))
        if dialog_type == 'file_request':
            self.error_dialog.add_action_button("NO",
                                                action=lambda *x: self.dialog_dismiss('{}_no'.format(dialog_type)))
        if dialog_type == 'add_friend':
            self.error_dialog.add_action_button("Cancel",
                                                action=lambda *x: self.dialog_dismiss('{}_cancel'.format(dialog_type)))
        self.error_dialog.open()

    def dialog_dismiss(self, dialog_type, userid='', filename=''):
        if dialog_type == 'login':
            self.root.ids.username.text = ''
            self.root.ids.password.text = ''
        elif dialog_type == 'connection':
            self.comm2server(self.host, self.server_port)
            self.comm2friendlist(self.host, self.server_port)
            reactor.listenUDP(self.msg_port, ChatClient(self))
        elif dialog_type == 'file_request':
            # Send ACK to friend, in format
            self.filerecv_flag.append([userid, filename])
            print('Agree to receive file from {}'.format(userid))
            for i in self.friend_list:
                i.display()
                if i.name == userid and i.is_online:
                    print('Send {}'.format('FILE_{}_ACK'.format(self.userid)))
                    if self.test_agent == 1:
                        self.chat_conn.write('FILE_{}_ACK'.format(self.userid), ('127.0.0.1', self.test_write_port1))
                    else:
                        self.chat_conn.write('FILE_{}_ACK'.format(self.userid), ('127.0.0.1', self.test_write_port2))
                    break
        elif dialog_type == 'add_friend':
            if self.root.ids.friend_name.text is None:
                return
            else:
                with open(self.friend_list_fn, 'a') as f:
                    f.write(self.root.ids.friend_name.text)
        self.error_dialog.dismiss()

    def get_time_picker_data(self, instance, time):
        self.root.ids.time_picker_label.text = str(time)
        self.previous_time = time

    def show_example_time_picker(self):
        self.time_dialog = MDTimePicker()
        self.time_dialog.bind(time=self.get_time_picker_data)
        if self.root.ids.time_picker_use_previous_time.active:
            try:
                self.time_dialog.set_time(self.previous_time)
            except AttributeError:
                pass
        self.time_dialog.open()

    def set_previous_date(self, date_obj):
        self.previous_date = date_obj
        self.root.ids.date_picker_label.text = str(date_obj)

    def show_example_date_picker(self):
        if self.root.ids.date_picker_use_previous_date.active:
            pd = self.previous_date
            try:
                MDDatePicker(self.set_previous_date,
                             pd.year, pd.month, pd.day).open()
            except AttributeError:
                MDDatePicker(self.set_previous_date).open()
        else:
            MDDatePicker(self.set_previous_date).open()

    def show_example_bottom_sheet(self):
        bs = MDListBottomSheet()
        bs.add_item("Here's an item with text only", lambda x: x)
        bs.add_item("Here's an item with an icon", lambda x: x,
                    icon='clipboard-account')
        bs.add_item("Here's another!", lambda x: x, icon='nfc')
        bs.open()

    def show_example_grid_bottom_sheet(self):
        bs = MDGridBottomSheet()
        bs.add_item("Facebook", lambda x: x,
                    icon_src='./assets/facebook-box.png')
        bs.add_item("YouTube", lambda x: x,
                    icon_src='./assets/youtube-play.png')
        bs.add_item("Twitter", lambda x: x,
                    icon_src='./assets/twitter.png')
        bs.add_item("Da Cloud", lambda x: x,
                    icon_src='./assets/cloud-upload.png')
        bs.add_item("Camera", lambda x: x,
                    icon_src='./assets/camera.png')
        bs.open()

    def bottom_navigation_remove_mobile(self, widget):
        # Removes some items from bottom-navigation demo when on mobile
        if DEVICE_TYPE == 'mobile':
            widget.ids.main_navigation.remove_widget(widget.ids.bottom_navigation_desktop_2)
        if DEVICE_TYPE == 'mobile' or DEVICE_TYPE == 'tablet':
            widget.ids.main_navigation.remove_widget(widget.ids.bottom_navigation_desktop_1)

    def show_example_snackbar(self, snack_type):
        if snack_type == 'simple':
            Snackbar(text="This is a snackbar!").show()
        elif snack_type == 'button':
            Snackbar(text="This is a snackbar", button_text="with a button!", button_callback=lambda *args: 2).show()
        elif snack_type == 'verylong':
            Snackbar(text="This is a very very very very very very very long snackbar!").show()

    def on_pause(self):
        return True

    def on_stop(self):
        pass


if __name__ == '__main__':
    IRC().run()
