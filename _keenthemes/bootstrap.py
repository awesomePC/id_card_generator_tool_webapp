from django.conf import settings
from .libs.theme import KTTheme
from pprint import pprint

# Core global bootstrap class
class KTBootstrap:

    # Init theme mode option from settings
    def initThemeMode():
        KTTheme.setModeSwitch(settings.KT_THEME_MODE_SWITCH_ENABLED)
        KTTheme.setModeDefault(settings.KT_THEME_MODE_DEFAULT)


    # Init theme direction option (RTL or LTR) from settings
    # Init RTL html attributes by checking if RTL is enabled.
    # This function is being called for the html tag
    def initThemeDirection():
        KTTheme.setDirection(settings.KT_THEME_DIRECTION)

        if KTTheme.isRtlDirection():
            KTTheme.addHtmlAttribute('html', 'direction', 'rtl')
            KTTheme.addHtmlAttribute('html', 'dir', 'rtl')
            KTTheme.addHtmlAttribute('html', 'style', 'direction: rtl')


    # Init layout html attributes and classes
    def initLayout():
        KTTheme.addHtmlAttribute('body', 'id', 'kt_app_body')
        KTTheme.addHtmlAttribute('body', 'data-kt-name', KTTheme.getName())


    # Main initialization
    def init():
        KTBootstrap.initThemeMode()
        KTBootstrap.initThemeDirection()
        KTBootstrap.initLayout()

        

        