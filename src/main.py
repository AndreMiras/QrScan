#!/usr/bin/env python
from __future__ import print_function, unicode_literals

import validators
from kivy.app import App
from kivy.clock import Clock
from kivy.core.clipboard import Clipboard
from kivy.logger import LOG_LEVELS, Logger
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from kivymd.icon_definitions import md_icons
from kivymd.theming import ThemeManager
from kivymd.toolbar import Toolbar
from raven import Client
from raven.conf import setup_logging
from raven.handlers.logging import SentryHandler

from version import __version__


class CodeType(object):
    TEXT = 0
    URL = 1
    CONTACT = 2

    @classmethod
    def from_data(cls, data):
        """
        Returns detected code type from input data.
        """
        code_type = cls.TEXT
        if validators.url(data):
            code_type = cls.URL
        elif data.startswith('BEGIN:VCARD'):
            code_type = cls.CONTACT
        else:
            code_type = cls.TEXT
        return code_type


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
        Binds `ZBarCam.on_codes()` event.
        """
        zbarcam = self.ids.zbarcam_id
        zbarcam.bind(codes=self.on_codes)

    def on_codes(self, zbarcam, codes):
        """
        Loads the first code data to the `QRFoundScreen.data_property`.
        """
        # going from codes found to no codes found state would also
        # trigger `on_codes`
        if not codes:
            return
        self.manager.transition.direction = 'left'
        self.manager.current = 'qrfound_screen'
        qrfound_screen = self.manager.current_screen
        code = codes[0]
        data = code.decode('utf8')
        qrfound_screen.data_property = data


class QRFoundScreen(SubScreen):

    data_property = StringProperty()
    title_property = StringProperty()
    icon_property = StringProperty()

    def __init__(self, **kwargs):
        super(QRFoundScreen, self).__init__(**kwargs)
        self._code_type = CodeType.TEXT
        self.map_dict = {
            CodeType.TEXT: ('Text', 'comment-text'),
            CodeType.URL: ('URL', 'link'),
            CodeType.CONTACT: ('Contact', 'account'),
        }

    def on_data_property(self, instance, value):
        """
        Updates `icon_property` and `title_property`.
        """
        self._code_type = CodeType.from_data(value)
        self.icon_property = self.icon()
        self.title_property = self.title()

    @property
    def code_type(self):
        return self._code_type

    def title(self):
        return self.map_dict[self.code_type][0]

    def icon(self):
        icon_name = self.map_dict[self.code_type][1]
        return "{}".format(md_icons[icon_name])

    def copy_to_clipboard(self):
        """
        Copies `data_property` to clipboard.
        """
        Clipboard.copy(self.data_property)


class DebugRavenClient(object):
    """
    The DebugRavenClient should be used in debug mode, it just raises
    the exception rather than capturing it.
    """

    def captureException(self):
        raise


def configure_sentry(in_debug=False):
    """
    Configure the Raven client, or create a dummy one if `in_debug` is `True`.
    """
    key = '6d7cf8f828fa4bc0b6837f9f33123ae9'
    # the public DSN URL is not available on the Python client
    # so we're exposing the secret and will be revoking it on abuse
    # https://github.com/getsentry/raven-python/issues/569
    secret = '828fc60c7d434d6d96a3ff2a07542224'
    project_id = '303227'
    dsn = 'https://{key}:{secret}@sentry.io/{project_id}'.format(
        key=key, secret=secret, project_id=project_id)
    if in_debug:
        client = DebugRavenClient()
    else:
        client = Client(dsn=dsn, release=__version__)
        # adds context for Android devices
        if platform == 'android':
            from jnius import autoclass
            Build = autoclass("android.os.Build")
            VERSION = autoclass('android.os.Build$VERSION')
            android_os_build = {
                'model': Build.MODEL,
                'brand': Build.BRAND,
                'device': Build.DEVICE,
                'manufacturer': Build.MANUFACTURER,
                'version_release': VERSION.RELEASE,
            }
            client.user_context({'android_os_build': android_os_build})
        # Logger.error() to Sentry
        # https://docs.sentry.io/clients/python/integrations/logging/
        handler = SentryHandler(client)
        handler.setLevel(LOG_LEVELS.get('error'))
        setup_logging(handler)
    return client


class MainApp(App):

    theme_cls = ThemeManager()

    def build(self):
        self.icon = "docs/images/icon.png"


if __name__ == '__main__':
    # when the -d/--debug flag is set, Kivy sets log level to debug
    level = Logger.getEffectiveLevel()
    in_debug = level == LOG_LEVELS.get('debug')
    client = configure_sentry(in_debug)
    try:
        MainApp().run()
    except Exception:
        if type(client) == Client:
            Logger.info(
                'Errors will be sent to Sentry, run with "--debug" if you '
                'are a developper and want to the error in the shell.')
        client.captureException()
