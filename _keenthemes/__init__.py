from pprint import pprint
from _keenthemes.bootstrap import KTBootstrap
from _keenthemes.libs.theme import KTTheme
import importlib.util
import sys

class KTLayout:

    # Initialize the bootstrap files and page layout
    def init(context):
        # Init the theme API
        KTTheme.init()

        # Set a default layout globally. Can be set in the page level view file as well.
        # See example in dashboards/views.py
        context.update({
            'layout': KTTheme.setLayout('default.html', context),
            #'layout': KTTheme.setLayout('default_header_layout.html', context),
            #'layout': KTTheme.setLayout('default_mini_sidebar_layout.html', context),
            #'layout': KTTheme.setLayout('default_overlay_layout.html', context),
        })

        # Init the base theme settings
        KTBootstrap.init()

        # Return context
        return context
