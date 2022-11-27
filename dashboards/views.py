from django.views.generic import TemplateView
from django.http import HttpResponse
from django.conf import settings
from django.urls import resolve
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from pprint import pprint
from django.shortcuts import render,redirect

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""

class DashboardsView(TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'pages/dashboards/index.html'

    # def get(self, request):
    #     return render(request,self.template_name)
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('isAuthenticated',False) is False:
            return redirect('/signin')
        else:
            return super(DashboardsView, self).get(request, *args, **kwargs)
    # Predefined function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        """
        # Example to get page name. Refer to dashboards/urls.py file.
        url_name = resolve(self.request.path_info).url_name

        if url_name == 'dashboard-2':
            # Example to override settings at the runtime
            settings.KT_THEME_DIRECTION = 'rtl'
        else:
            settings.KT_THEME_DIRECTION = 'ltr'
        """

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # Include vendors and javascript files for dashboard widgets
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        # request=context['view'].request
        # if request.session.get('isAuthenticated',False) is False:
        #     return redirect('/signin')
        context['session']=self.request.session
        return context
