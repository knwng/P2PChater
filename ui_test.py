# -*- coding: utf-8 -*-
from Backend import *
from config import *
import time
import os,sys, time

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.widget import Widget
from kivy.utils import get_color_from_hex

from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem, OneLineListItem, TwoLineListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase, NavigationDrawerIconButton
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker
from kivymd.toolbar import Toolbar
from kivymd.color_definitions import colors
from kivymd.textfields import MDTextField

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
                        MDTextField:
                            hint_text: "You can put any widgets here"
                MDBottomNavigationItem:
                    name: 'Profile'
                    text: "Profile"
                    icon: 'alert'
                    id: profile
                    BoxLayout:
                        orientation: 'vertical'
                        size_hint_y: None
                        padding: dp(48)
                        spacing: 10
                        MDTextField:
                            hint_text: "Hello again"   
        Screen:
            name: 'chatroom'
            Toolbar:
                id: chatroom_toolbar
                title: 'ChatRoom'
                pos_hint: {'center_x': 0.5, 'top': 1}
                size_hint: 1, 0.1
                md_bg_color: get_color_from_hex(colors['DeepPurple']['A400'])
                background_palette: 'DeepPurple'
                background_hue: 'A400'
                left_action_items: [['arrow-left', app.back_to_mainpage]]
            FloatLayout:
                orientation: 'horizontal'
                pos_hint: {'left': 0, 'bottom': 0}
                size_hint: 1, 0.1
                MDIconButton:
                    icon: 'file'
                    pos_hint: {'left': 0.3, 'center_y': 0.5}
                    # disabled: disable_the_buttons.active
                MDTextField:
                    id: chatroom_input
                    required: True
                    multiline: True
                    color_mode: 'accent'
                    pos_hint: {'center_x': 0.5, 'center_y': 0.5}
                    size_hint: 0.6, 0.9
                MDRaisedButton:
                    text: "Send"
                    elevation_normal: 2
                    opposite_colors: True
                    pos_hint: {'right': 0.96, 'center_y': 0.5}
                    size_hint: 0.1, 0.4
                    # disabled: disable_the_buttons.active
            ScrollView:
                do_scroll_x: False
                id: chatroom_msg
                pos_hint: {'center_x': 0.5, 'top': 0.9}
                size_hint: 1, 0.7
                                       
'''

class HackedDemoNavDrawer(MDNavigationDrawer):
    # DO NOT USE
    def add_widget(self, widget, index=0):
        if issubclass(widget.__class__, BaseListItem):
            self._list.add_widget(widget, index)
            if len(self._list.children) == 1:
                widget._active = True
                self.active_item = widget
            # widget.bind(on_release=lambda x: self.panel.toggle_state())
            widget.bind(on_release=lambda x: x._set_active(True, list=self))
        elif issubclass(widget.__class__, NavigationDrawerHeaderBase):
            self._header_container.add_widget(widget)
        else:
            super(MDNavigationDrawer, self).add_widget(widget, index)


class KitchenSink(App):
    theme_cls = ThemeManager()
    previous_date = ObjectProperty()
    title = "KivyMD Kitchen Sink"
    msg = StringProperty('')
    login_conn = None
    friendlist_conn = None
    friend_list = []
    curr_proc_friend = None
    curr_generate_client = None
    login_status = False

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
        # self.theme_cls.theme_style = 'Dark'

        # main_widget.ids.text_field_error.bind(
        #     on_text_validate=self.set_error_message,
        #     on_focus=self.set_error_message)

        self.bottom_navigation_remove_mobile(main_widget)
        self.host = '166.111.140.14'
        self.server_port = 8000
        self.listen_port = 12500
        self.comm2server(self.host, self.server_port)
        self.comm2friendlist(self.host, self.server_port)
        reactor.listenTCP(self.listen_port, RequestServerFactory(self))
        return main_widget

    # Network
    def comm2server(self, dst_host, dst_port):
        reactor.connectTCP(dst_host, dst_port, LoginClientFactory(self))
        return

    def comm2friendlist(self, dst_host, dst_port):
        reactor.connectTCP(dst_host, dst_port, FriendlistClientFactory(self))
        return

    def comm2chat(self, dst_host, dst_port):
        reactor.connectTCP(dst_host, dst_port, ChatClientFactory(self))
        return

    def on_login_conn(self, conn):
        self.login_conn = conn

    def on_friendlist_conn(self, conn):
        self.friendlist_conn = conn

    def on_chatclient_conn(self, conn):
        self.friend_list[self.curr_generate_client].chat_client = conn

    def login(self, username, password, *args):
        if self.login_conn:
            self.login_conn.write('{}_{}'.format(username, password).encode('utf-8'))
        else:
            self.show_connection_error_dialog()
        return

    def login_callback(self, FLAG):
        if FLAG:
            # self.login_conn.loseConnection()
            # del self.login_conn
            self.login_status = True
            self.root.ids.scr_mngr.current = 'mainpage'
            self.get_friendlist()
            Clock.schedule_interval(self.get_friendlist, 1)
        else:
            self.show_connection_error_dialog()

    def get_friendlist(self, *largs):
        with file(friend_list_fn, 'r') as f:
            flt = f.readlines()
        flt = [x[0:-1] for x in flt if re.match(pattern_id, x) is not None]
        # print('get friend list: {}'.format(flt))
        self.friend_list = []
        for i in flt:
            self.friend_list.append(Friends(name=i))
        self.curr_proc_friend = 0
        self.friendlist_conn.write('q{}'.format(self.friend_list[0].name))

    def query_friend(self, id):
        self.friendlist_conn.write(id.encode('utf-8'))
        self.friendlist_conn.loseConnection()
        return

    def proc_friend_list(self, flag, msg=None):
        self.friend_list[self.curr_proc_friend].is_online = flag
        if flag:
            self.friend_list[self.curr_proc_friend].ip = msg
        self.curr_proc_friend += 1
        if self.curr_proc_friend < len(self.friend_list):
            self.friendlist_conn.write('q{}'.format(self.friend_list[self.curr_proc_friend].name))
        else:
            self.show_friend_card()
        return

    def back_to_mainpage(self, *args):
        self.root.ids.scr_mngr.current = 'mainpage'
        return


    def show_friend_card(self):
        self.root.ids.ml.clear_widgets()
        for i in self.friend_list:
            if i.is_online:
                listwidget = OneLineListItem(text=i.name,
                                             theme_text_color='Custom',
                                             text_color=get_color_from_hex(colors['Amber']['700']),
                                             on_release=self.chatwith)
                # iconwidget = IconLeftSampleWidget(icon='account', id='icon_{}'.format(i.name))
                iconwidget = IconLeftSampleWidget(icon='account')
                listwidget.add_widget(iconwidget)
                self.root.ids.ml.add_widget(listwidget)
            else:
                listwidget = OneLineListItem(text=i.name,
                                             theme_text_color='Custom',
                                             on_release=self.chatwith)
                # iconwidget = IconLeftSampleWidget(icon='account-off', id='icon_{}'.format(i.name))
                iconwidget = IconLeftSampleWidget(icon='account-off')
                listwidget.add_widget(iconwidget)
                self.root.ids.ml.add_widget(listwidget)
        return

    def chatwith(self, instance):
        print('Widget {} are pressed'.format(instance.text))
        for i in range(len(self.friend_list)):
            if self.friend_list[i].name == instance.text:
                if self.friend_list[i].is_online is False:
                    self.show_offline_error_dialog()
                    return
                elif self.friend_list[i].is_use is False:
                    self.friend_list[i].is_use = True
                    self.curr_generate_client = i
                    self.comm2chat(self.host, self.listen_port)
                self.show_chat_window(self.friend_list[i].name)
                return


    def show_chat_window(self, id):
        self.root.ids.chatroom_toolbar.title = 'Chat With {}'.format(id)
        self.root.ids.scr_mngr.current = 'chatroom'
        return

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

    def get_username_passwd(self):
        username = self.root.ids.username.text
        password = self.root.ids.password.text
        # print('Username: {}'.format(username))
        # print('Password: {}'.format(password))
        # for i in self.root.ids:
        #     print('Current Widget: {}'.format(i))
        if username == '2014010622' and password == 'net2017':
            self.login(username, password)
        else:
            self.show_login_error_dialog()

    def show_offline_error_dialog(self):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text='Friend is offline',
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.offline_error_dialog = MDDialog(title="This friend is currently offline",
                                           content=content,
                                           size_hint=(.8, None),
                                           height=dp(200),
                                           auto_dismiss=False)
        self.offline_error_dialog.add_action_button("OK",
                                                  action=lambda *x: self.offline_error_dialog_dismiss())
        self.offline_error_dialog.open()

    def offline_error_dialog_dismiss(self):
        self.offline_error_dialog.dismiss()

    def show_login_error_dialog(self):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text='Please Check your username and password',
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.login_error_dialog = MDDialog(title="Wrong username/password!",
                                           content=content,
                                           size_hint=(.8, None),
                                           height=dp(200),
                                           auto_dismiss=False)
        self.login_error_dialog.add_action_button("OK",
                                                  action=lambda *x: self.login_error_dialog_dismiss())
        self.login_error_dialog.open()

    def login_error_dialog_dismiss(self):
        self.root.ids.username.text = ''
        self.root.ids.password.text = ''
        self.login_error_dialog.dismiss()

    def show_connection_error_dialog(self):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text='Please Check your Internet Connection',
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.connection_error_dialog = MDDialog(title="Connection Failed",
                                                content=content,
                                                size_hint=(.8, None),
                                                height=dp(200),
                                                auto_dismiss=False)
        self.connection_error_dialog.add_action_button("OK",
                                                       action=lambda *x: self.connection_error_dialog_dismiss())
        self.connection_error_dialog.open()

    def connection_error_dialog_dismiss(self):
        self.connection_error_dialog.dismiss()
        self.comm2server(self.host, self.server_port)
        self.comm2friend(self.host, self.server_port)
        reactor.listenTCP(self.listen_port, RequestServerFactory(self))

    def show_example_dialog(self):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="This is a dialog with a title and some text. "
                               "That's pretty awesome right!",
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="This is a test dialog",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        self.dialog.add_action_button("Dismiss",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    def show_example_long_dialog(self):
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text="Lorem ipsum dolor sit amet, consectetur "
                               "adipiscing elit, sed do eiusmod tempor "
                               "incididunt ut labore et dolore magna aliqua. "
                               "Ut enim ad minim veniam, quis nostrud "
                               "exercitation ullamco laboris nisi ut aliquip "
                               "ex ea commodo consequat. Duis aute irure "
                               "dolor in reprehenderit in voluptate velit "
                               "esse cillum dolore eu fugiat nulla pariatur. "
                               "Excepteur sint occaecat cupidatat non "
                               "proident, sunt in culpa qui officia deserunt "
                               "mollit anim id est laborum.",
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="This is a long test dialog",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        self.dialog.add_action_button("Dismiss",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

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

    '''
    def set_error_message(self, *args):
        if len(self.root.ids.text_field_error.text) == 2:
            self.root.ids.text_field_error.error = True
        else:
            self.root.ids.text_field_error.error = False
    '''

    def on_pause(self):
        return True

    def on_stop(self):
        pass


class AvatarSampleWidget(ILeftBody, Image):
    pass


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass


if __name__ == '__main__':
    KitchenSink().run()
