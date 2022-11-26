from django.conf import settings
from pprint import pprint
import os
from django.templatetags.static import static
from importlib import import_module, util

# Core theme class
class KTTheme:

    # Variables
    modeSwitchEnabled = False
    modeDefault = 'light'

    direction = 'ltr'

    htmlAttributes = {}
    htmlClasses = {}

    # Keep page level assets
    javascriptFiles = []
    cssFiles = []
    vendorFiles = []


    def init():
        KTTheme.htmlAttributes = {}
        KTTheme.htmlClasses = {}

        KTTheme.javascriptFiles = []
        KTTheme.cssFiles = []
        KTTheme.vendorFiles = []


    # Get product name
    def getName():
        return settings.KT_THEME


    # Add HTML attributes by scope
    def addHtmlAttribute(scope, name, value):
        KTTheme.htmlAttributes.setdefault(scope, {})
        KTTheme.htmlAttributes[scope][name] = value


    # Add multiple HTML attributes by scope
    def addHtmlAttributes(scope, attributes):
        KTTheme.htmlAttributes.setdefault(scope, {})
        for key in attributes:
            KTTheme.htmlAttributes[scope][key] = attributes[key]


    # Add HTML class by scope
    def addHtmlClass(scope, value):
        KTTheme.htmlClasses.setdefault(scope, [])
        if value not in KTTheme.htmlClasses[scope]:
            KTTheme.htmlClasses[scope].append(value)


    # Print HTML attributes for the HTML template
    def printHtmlAttributes(scope):
        attributes = []
        if scope in KTTheme.htmlAttributes:
            for key in KTTheme.htmlAttributes[scope]:
                attributes.append('{}="{}"'.format(key, KTTheme.htmlAttributes[scope][key]))

        return ' '.join(attributes)


    # Print HTML classes for the HTML template
    def printHtmlClasses(scope, full = True):
        if not KTTheme.htmlClasses:
            return ''

        classes = ''
        if scope in KTTheme.htmlClasses:
            classes = ' '.join(KTTheme.htmlClasses[scope])

        if (full):
            return 'class="{}"'.format(classes)
        else:
            return classes


    # Get SVG icon content
    def getSvgIcon(path, classNames = 'svg-icon', folder = 'media/icons/'):
        # Reference to current folder
        svg = open('.' + KTTheme.asset(folder + path)).read()
        output = '<span class="{}">{}</span>'.format(classNames, svg)
        return output


    # Get an assets path in assets folder by path
    def asset(path):
        return static(path)


    # Set dark mode enabled status
    def setModeSwitch(flag):
        KTTheme.modeSwitchEnabled = flag


    # Check dark mode status
    def isModeSwitchEnabled():
        return KTTheme.modeSwitchEnabled


    # Set the mode to dark or light
    def setModeDefault(mode):
        KTTheme.modeDefault = mode


    # Get current mode
    def getModeDefault():
        return KTTheme.modeDefault

    # Set style direction
    def setDirection(direction):
        KTTheme.direction = direction


    # Get style direction
    def getDirection():
        return KTTheme.direction


    # Check if style direction is RTL
    def isRtlDirection():
        return KTTheme.direction.lower() == 'rtl'


    # Extend CSS file name with RTL or dark mode
    def extendCssFilename(path):
        if KTTheme.isRtlDirection():
            path = path.replace('.css', '.rtl.css')

        return path


    # Include favicon from settings
    def includeFavicon():
        # Use static() to use builtin function for assets folder
        # Refer in _keenthemes/settings.py for STATIC_URL settings
        return static(settings.KT_THEME_ASSETS['favicon'])


    # Include the fonts from settings
    def includeFonts():
        content = ''
        for url in settings.KT_THEME_ASSETS['fonts']:
            content += '<link rel="stylesheet" href="{}">'.format(url)

        return content


    # Get the global assets
    def getGlobalAssets(type):
        files = []
        for file in settings.KT_THEME_ASSETS[type]:
            if type == 'css':
                # Modify css file name suffix based on the RTL or dark mode settings
                files.append(KTTheme.extendCssFilename(file))
            else:
                files.append(file)

        return files


    # Add multiple vendors to the page by name. Refer to settings.KT_THEME_VENDORS
    def addVendors(vendors):
        for value in vendors:
            # Skip duplicate entry
            if value not in KTTheme.vendorFiles:
                KTTheme.vendorFiles.append(value)


    # Add single vendor to the page by name. Refer to settings.KT_THEME_VENDORS
    def addVendor(vendor):
        # Skip duplicate entry
        if vendor not in KTTheme.vendorFiles:
            KTTheme.vendorFiles.append(vendor)


    # Add custom javascript file to the page
    def addJavascriptFile(file):
        # Skip duplicate entry
        if file not in KTTheme.javascriptFiles:
            KTTheme.javascriptFiles.append(file)


    # Add custom CSS file to the page
    def addCssFile(file):
        # Skip duplicate entry
        if file not in KTTheme.cssFiles:
            KTTheme.cssFiles.append(file)


    # Get vendor files from settings. Refer to settings.KT_THEME_VENDORS
    def getVendors(type):
        files = []
        for vendor in KTTheme.vendorFiles:
            # Check if vendor exist in the settings
            if type in settings.KT_THEME_VENDORS[vendor]:
                # Skip duplicate entry
                if settings.KT_THEME_VENDORS[vendor][type] not in files:
                    for path in settings.KT_THEME_VENDORS[vendor][type]:
                        # add static url to local file paths, skip for external urls
                        files.append(KTTheme.addStatic(path))

        return files


    # Set the current page layout and init the layout bootstrap file
    def setLayout(view, context = {}):
        KTTheme.htmlAttributes = {}
        KTTheme.htmlClasses = {}

        layout = os.path.splitext(view)[0]
        layout = layout.split('/')[0]

        # Get module path
        module = '_templates.{}._bootstrap.{}'.format(settings.KT_THEME_LAYOUT_DIR.replace('/', '.'), layout)

        # Check if the bootstrap file is exist
        if not util.find_spec(module) == None:
            # Auto import and init the default bootstrap.py file from the theme
            KTBootstrap = KTTheme.importClass(module, 'KTBootstrap{}'.format(layout.title().replace('-', '')))
            KTBootstrap.init(context)
        else:
            module = '_templates.{}._bootstrap.default'.format(settings.KT_THEME_LAYOUT_DIR.replace('/', '.'))
            KTBootstrap = KTTheme.importClass(module, 'KTBootstrapDefault')
            KTBootstrap.init(context)

        return '{}/{}'.format(settings.KT_THEME_LAYOUT_DIR, view)


    # Import a module by string
    def importClass(fromModule, importClassName):
        pprint('Loading {} from {}'.format(importClassName, fromModule))
        module = import_module(fromModule)
        return getattr(module, importClassName)


    def addStatic(path):
        if '//' in path:
            return path
        return KTTheme.asset(path)