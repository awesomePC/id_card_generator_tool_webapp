from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from tasks.models import Tasks
from annotation.models import LanguageHub, FontHub, WordAnnotation
from django.shortcuts import redirect

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class AnnotateWordLevelView(TemplateView):
    template_name = 'pages/annotate/wordlevel.html'
    task_id = 0
    def dispatch(self, request, id, *args, **kwargs):
        if request.session.get('isAuthenticated',False) is False:
            return redirect('/signin')
        else:
            self.task_id = id
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
        # task_id from request
        task_id = self.task_id
        context['task_id'] = task_id
        if task_id != 0:
            context['isAnnoExist'] = int(True)
            context['annotations'] = []
            annotations = WordAnnotation.objects.filter(task_id = task_id)
            for annotation in annotations:
                temp = {}
                temp['word_index'] = annotation.word_index
                temp['text'] = annotation.text
                temp['font_id'] = int(annotation.font_id)
                temp['lang_id'] = int(annotation.lang_id)
                temp['is_bold'] = int(annotation.is_bold)
                temp['is_italic'] = int(annotation.is_italic)
                temp['box_coordinates'] = annotation.box_coordinates
                context['annotations'].append(temp)
        else:
            context['isAnnoExist'] = int(False)
       
        context['showTask']=True
        userId=self.request.session.get('user',None)['id']
        context['tasks'] = Tasks.objects.filter(CreateByUserId_id=userId)

        # select all languages
        languages = LanguageHub.objects.all()
        langs = []
        for lan in languages:
            temp = {}
            temp['id'] = lan.id
            temp['name'] = lan.name
             # select all fonts according to language
            fonts = FontHub.objects.filter(lang_id = lan.id)
            fons = []
            for fon in fonts:
                tem = {}
                tem['id'] = fon.id
                tem['name'] = fon.name
                fons.append(tem)
            temp['fonts'] = fons
            langs.append(temp)
        context['languages'] = langs
       
        return context
