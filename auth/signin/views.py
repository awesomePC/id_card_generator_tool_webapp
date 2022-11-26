from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class AuthSigninView(TemplateView):
    template_name = 'pages/auth/signin.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/authentication/sign-in/general.js')

        # Define the layout for this module
        # _templates/layout/auth.html
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })

        request=context['view'].request
        message=request.session.get('message',None)
        request.session.clear()
        context['message']=message
        return context
