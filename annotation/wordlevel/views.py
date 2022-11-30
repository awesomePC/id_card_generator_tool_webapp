from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from tasks.models import Tasks

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class AnnotateWordLevelView(TemplateView):
    template_name = 'pages/annotate/wordlevel.html'
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('isAuthenticated',False) is False:
            return redirect('/signin')
        else:
            return super(AnnotateWordLevelView, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('/annotate/js/fabric.min.js')
        KTTheme.addJavascriptFile('/annotate/js/FabricJsHistory.js')
        KTTheme.addJavascriptFile('/annotate/js/wordlevel.js')
        KTTheme.addCssFile('/annotate/css/style.css')
        id=self.request.GET.get('id',None)
        if id !=None:
            rec=Tasks.objects.get(id=id)
            if rec != None:
                context['image']=rec.MainImageFile
        else:
            context['showTask']=True
            userId=self.request.session.get('user',None)['id']
            context['tasks'] = Tasks.objects.filter(CreateByUserId_id=userId)
        return context
