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
    task_id = 0
    def dispatch(self, request, id, *args, **kwargs):
        if request.session.get('isAuthenticated',False) is False:
            return redirect('/signin')
        else:
            self.task_id = id
            return super(AnnotateMainView, self).get(request, *args, **kwargs)
       
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
        task_id = self.task_id
        context['task_id'] = task_id
        if task_id != 0:
            context['isAnnoExist'] = int(True)
            context['annotations'] = []
            annotations = LineAnnotation.objects.filter(task_id = task_id)
            for annotation in annotations:
                temp = {}
                temp['line_index'] = annotation.line_index
                temp['type'] = annotation.type
                temp['text'] = annotation.text
                temp['is_fixed_text'] = int(annotation.is_fixed_text)
                temp['is_render_text'] = int(annotation.is_render_text)
                temp['box_coordinates'] = annotation.box_coordinates
                temp['key_label'] = annotation.key_label
                temp['dict_id'] = annotation.dict_id
                context['annotations'].append(temp)
        else:
            context['isAnnoExist'] = int(False)
        context['showTask']=True
        userId=self.request.session.get('user',None)['id']
        context['tasks'] = Tasks.objects.filter(CreateByUserId_id=userId)
      
        context['dictionarys'] = list(DictionaryHub.objects.values("id", "name"))
        return context
