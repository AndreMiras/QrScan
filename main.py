#!/usr/bin/env python
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.theming import ThemeManager
from kivymd.toolbar import Toolbar


class CustomToolbar(Toolbar):

    def __init__(self, **kwargs):
        super(CustomToolbar, self).__init__(**kwargs)
        Clock.schedule_once(self.load_default_buttons)

    def load_default_buttons(self, dt=None):
        self.left_action_items = [['menu', lambda x: None]]
        self.right_action_items = [['dots-vertical', lambda x: None]]

    def load_back_button(self, function):
        # lambda x: app.root.toggle_nav_drawer()
        self.left_action_items = [['arrow-left', lambda x: function()]]


class QRScanScreen(Screen):

    def __init__(self, **kwargs):
        super(QRScanScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._after_init)

    def _after_init(self, dt):
        """
        Binds `ZBarCam.on_symbols()` event.
        """
        zbarcam = self.ids.zbarcam_id
        zbarcam.bind(symbols=self.on_symbols)

    def on_symbols(self, zbarcam, symbols):
        """
        Loads the first symbol data to the `QRFoundScreen.data_property`.
        """
        # going from symbols found to no symbols found state would also
        # trigger `on_symbols`
        if not symbols:
            return
        self.manager.transition.direction = 'left'
        self.manager.current = 'qrfound_screen'
        qrfound_screen = self.manager.current_screen
        symbol = symbols[0]
        qrfound_screen.data_property = symbol.data


class QRFoundScreen(Screen):

    data_property = StringProperty()

    def on_back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'qrscan_screen'

    def on_enter(self):
        """
        Loads the toolbar back button.
        """
        app = App.get_running_app()
        app.root.ids.toolbar_id.load_back_button(self.on_back)

    def on_leave(self):
        """
        Loads the toolbar default button.
        """
        app = App.get_running_app()
        app.root.ids.toolbar_id.load_default_buttons()


class MainApp(App):
    theme_cls = ThemeManager()


if __name__ == '__main__':
    MainApp().run()
