from _keenthemes.libs.theme import KTTheme

"""
This is an entry and Bootstrap class for the theme level.
The init() function will be called in _keenthemes/__init__.py
"""
class KTBootstrapSystem:

    def init(context):
        KTTheme.addHtmlClass('body', 'app-blank')
        KTTheme.addHtmlClass("body", "bgi-size-cover bgi-position-center bgi-no-repeat");
