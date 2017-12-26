from kivy.uix.image import Image
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase, NavigationDrawerIconButton
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem, OneLineListItem, TwoLineListItem
from kivymd.button import MDIconButton
from kivymd.selectioncontrols import MDCheckbox
from kivymd.color_definitions import colors
from kivymd.card import MDCard, MDSeparator
from kivymd.label import MDLabel


class MessageCard(object):
    def __init__(self, type, title, body, idx, parent_shape):
        """

        :param type: card type, 'left' or 'right'
        :param title: text in title
        :param body: text in body
        :param idx: idx of message card, to set position
        :param parent_shape: parent widget shape in [width, height], to compute position
        """
        print("MessageCard's parent's shape: {}".format(parent_shape))
        print('Color: {}'.format(get_color_from_hex(colors['Blue']['200'])))
        if type == 'left':
            self.message_card = MDCard(size_hint=(None, None),
                                       size=(dp(160), dp(90)),
                                       left=dp(60),
                                       top=dp(parent_shape[1]-10-100*idx),
                                       md_bg_color=get_color_from_hex(colors['Blue']['200']),
                                       background_palette='DeepPurple',
                                       background_hue='A400',
                                       border_radius=dp(10))
        elif type == 'right':
            self.message_card = MDCard(size_hint=(None, None),
                                       size=(dp(160), dp(90)),
                                       right=dp(parent_shape[0]-80),
                                       top=dp(parent_shape[1]-10-100*idx),
                                       md_bg_color=get_color_from_hex(colors['Green']['200']),
                                       border_radius=dp(10))
        else:
            raise Exception, 'Card Type Error'

        msgbox = BoxLayout(# id='msgcard_box',
                           orientation='vertical',
                           padding=dp(8))
        # msgbox.add_widget(MDLabel(# id='msgcard_title',
        #                           text=title,
        #                           theme_text_color='Secondary',
        #                           font_stype='Title',
        #                           size_hint_y=None,
        #                           height=dp(32)))
        # msgbox.add_widget(MDSeparator(height=dp(1)))
        msgbox.add_widget(MDLabel(# id='msgcard_body',
                                  text=body,
                                  theme_text_color='Primary'))
        self.message_card.add_widget(msgbox)

    def get_card(self):
        return self.message_card


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


class AvatarSampleWidget(ILeftBody, Image):
    pass


class IconLeftSampleWidget(ILeftBodyTouch, MDIconButton):
    pass


class IconRightSampleWidget(IRightBodyTouch, MDCheckbox):
    pass