from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from tasks.models import Tasks
from annotation.models import DictionaryHub, LineAnnotation, WordAnnotation
from django.shortcuts import redirect
"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class AnnotateMainView(TemplateView):
    template_name = 'pages/annotate/index.html'
    ID = 0
    def dispatch(self, request, id, *args, **kwargs):
        if request.session.get('isAuthenticated',False) is False:
            return redirect('/signin')
        else:
            self.ID = id
            return super(AnnotateMainView, self).get(request, id, *args, **kwargs)
       
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('/annotate/js/fabric.min.js')
        KTTheme.addJavascriptFile('/annotate/js/FabricJsHistory.js')
        KTTheme.addJavascriptFile('/annotate/js/script.js')
        KTTheme.addCssFile('/annotate/css/style.css')
        # task_id from request
        id = self.ID
        # id=self.request.GET.get('id',None)
        if id != 0:
            context['isAnnoExist'] = True
            rec=Tasks.objects.get(id=id)
            context['annotations'] = list(LineAnnotation.objects.values("line_index","type", 
                                    "text", "is_fixed_text", "is_render_text","box_coordinates", "key_value", "dict_id"))
            #  values("id", "name"))
        else:
            context['isAnnoExist'] = False
        context['showTask']=True
        userId=self.request.session.get('user',None)['id']
        context['tasks'] = Tasks.objects.filter(CreateByUserId_id=userId)
      
        context['dictionarys'] = list(DictionaryHub.objects.values("id", "name"))
        return context
