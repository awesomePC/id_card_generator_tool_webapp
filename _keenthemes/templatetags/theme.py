from django.utils.safestring import mark_safe
from django import template
from _keenthemes.libs.theme import KTTheme
from django.conf import settings
from pprint import pprint

register = template.Library()

# Register tags as an adapter for the Theme class usage in the HTML template

@register.simple_tag
def includeFonts():
    return mark_safe(KTTheme.includeFonts())

@register.simple_tag
def includeFavicon():
    return mark_safe(KTTheme.includeFavicon())

@register.simple_tag
def getSvgIcon(path, classNames = 'svg-icon', folder = 'media/icons/'):
    return mark_safe(KTTheme.getSvgIcon(path, classNames, folder))

@register.simple_tag
def printHtmlClasses(scope):
    return mark_safe(KTTheme.printHtmlClasses(scope))

@register.simple_tag
def printHtmlAttributes(scope):
    return mark_safe(KTTheme.printHtmlAttributes(scope))

@register.simple_tag
def getGlobalAssets(type):
    return KTTheme.getGlobalAssets(type)

@register.simple_tag
def getCustomJs():
    return KTTheme.javascriptFiles

@register.simple_tag
def getCustomCss():
    return KTTheme.cssFiles

@register.simple_tag
def getVendors(type):
    return KTTheme.getVendors(type)

@register.simple_tag
def isRtlDirection():
    return KTTheme.isRtlDirection()

@register.simple_tag
def asset(path):
    return KTTheme.asset(path)

@register.simple_tag
def getModeDefault():
    return KTTheme.getModeDefault()

@register.simple_tag
def addHtmlAttribute(scope, name, value):
    KTTheme.addHtmlAttribute(scope, name, value)
    return ''

@register.simple_tag
def addHtmlAttributes(scope, attributes):
    KTTheme.addHtmlAttributes(scope, attributes)
    return ''

@register.simple_tag
def addHtmlClass(scope, value):
    KTTheme.addHtmlClass(scope, value)
    return ''

@register.simple_tag
def getHtmlAttribute(scope, attribute):
    return KTTheme.htmlAttributes[scope][attribute]
