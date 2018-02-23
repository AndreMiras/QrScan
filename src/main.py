#!/usr/bin/env python
from kivy.app import App
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.theming import ThemeManager
from kivymd.toolbar import Toolbar

from version import __version__


class CustomToolbar(Toolbar):
    """
    Toolbar with helper method for loading default/back buttons.
    """

    def __init__(self, **kwargs):
        super(CustomToolbar, self).__init__(**kwargs)
        Clock.schedule_once(self.load_default_buttons)

    def load_default_buttons(self, dt=None):
        app = App.get_running_app()
        self.left_action_items = [
            ['menu', lambda x: app.root.toggle_nav_drawer()]]
        self.right_action_items = [
            ['dots-vertical', lambda x: app.root.toggle_nav_drawer()]]

    def load_back_button(self, function):
        self.left_action_items = [['arrow-left', lambda x: function()]]


class SubScreen(Screen):
    """
    Helper parent class for updating toolbar on enter/leave.
    """

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


class AboutScreen(SubScreen):

    project_page_property = StringProperty(
        "https://github.com/AndreMiras/QrScan")
    about_text_property = StringProperty()

    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)
        Clock.schedule_once(lambda dt: self.load_about())

    def load_about(self):
        self.about_text_property = "" + \
            "QrScan version: %s\n" % (__version__) + \
            "Project source code and info available on GitHub at:\n" + \
            "[color=00BFFF][ref=github]" + \
            self.project_page_property + \
            "[/ref][/color]"


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


class QRFoundScreen(SubScreen):

    data_property = StringProperty()

    def copy_to_clipboard(self):
        """
        Copies `data_property` to clipboard.
        """
        Clipboard.copy(self.data_property)


class MainApp(App):
    theme_cls = ThemeManager()


if __name__ == '__main__':
    MainApp().run()
