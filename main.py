#!/usr/bin/env python
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivymd.theming import ThemeManager


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
        self.manager.current = 'qrfound_screen'
        qrfound_screen = self.manager.current_screen
        symbol = symbols[0]
        qrfound_screen.data_property = symbol.data


class QRFoundScreen(Screen):
    data_property = StringProperty()


class MainApp(App):
    theme_cls = ThemeManager()


if __name__ == '__main__':
    MainApp().run()
