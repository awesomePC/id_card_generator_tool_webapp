from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from ..models import Projects

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class ProjectListView(TemplateView):
    template_name = 'pages/projects/index.html'
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('isAuthenticated',False) is False:
            return redirect('/signin')
        else:
            return super(ProjectListView, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # KTTheme.addJavascriptFile('js/custom/authentication/sign-up/general.js')
        request=context['view'].request
        userid=request.session.get('user',None)['id']
        recs=Projects.objects.filter(CreateByUserId_id=userid).order_by('-id')
        context['count']=recs.count()
        context['projects']=recs
        return context
