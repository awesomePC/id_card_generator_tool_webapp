from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from tasks.models import Tasks
from annotation.models import LineAnnotation,LineRendering,DictionaryHub
from django.shortcuts import redirect
from decimal import Decimal

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class AnnotatePreviewView(TemplateView):
    template_name = 'pages/annotate/preview.html'
    task_id = 0
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('isAuthenticated',False) is False:
            return redirect('/signin')
        else: 
            return super(AnnotatePreviewView, self).get(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('/annotate/js/fabric.min.js')
        KTTheme.addJavascriptFile('/annotate/js/FabricJsHistory.js')
        # KTTheme.addJavascriptFile('/annotate/js/wordlevel.js') 
        KTTheme.addJavascriptFile('/annotate/js/preview.js') 
        KTTheme.addCssFile('/annotate/css/style.css')

        # task_id from request
        #
        task_id=self.request.GET.get('id',None)  
        userId=self.request.session.get('user',None)['id']

        
       
 
        context['previewAnnotations'] = []
        if task_id is not None and task_id != 0: 
            task_Obj=Tasks.objects.get(id=task_id)

           # insert dict dummy data
            dict_Obj , created_dict = DictionaryHub.objects.update_or_create(
            name='TestDictionary', 
            type="text",
            file="./resources/dict/english_person_name_cnt-50.txt",
            created_by_user_id=userId
            )
           
            # if already dict_Obj exists
            # dict_Obj=DictionaryHub.objects.get(created_by_user_id=userId)
            
            # insert line_annotation, line rendering dummy data
            lineAnn_obj , created_line_annotation = LineAnnotation.objects.update_or_create(
            type='text', 
            text='Temporary',
            task=task_Obj,
            dict=dict_Obj
            )
           
            LineRendering.objects.update_or_create(
            line=lineAnn_obj, 
            generated_line_image='images/dummy.jpg',
            left=32.73748779296875,
            top=282.2843218761455,
            height = 43.97419354838712,
            width = 133
            )
            LineRendering.objects.update_or_create(
            line=lineAnn_obj, 
            generated_line_image='images/dummy.jpg',
            left=533.3374938964844,
            top=58.41,
            height = 31.97419354838712,
            width = 90
            )
            LineRendering.objects.update_or_create(
            line=lineAnn_obj, 
            generated_line_image='images/dummy.jpg',
            left=21.33749389648437,
            top=10.443852667934385,
            height = 37.97771260997067,
            width = 127
            )


            annotations = LineAnnotation.objects.filter(task_id = task_id)
           
            for annotation in annotations: 
                previewAnnotation = LineRendering.objects.filter(line_id = annotation.id) 
                for prevannotation in previewAnnotation: 
                    temp = {}
                    temp['image'] = str(prevannotation.generated_line_image)
                    temp['left'] = float(prevannotation.left)
                    temp['top'] = float(prevannotation.top)
                    temp['height'] = float(prevannotation.height)
                    temp['width'] = float(prevannotation.width)
                    context['previewAnnotations'].append(temp)
        else:
            
            task_id=0 
      
        # if id !=None:
        #     rec=Tasks.objects.get(id=id)
        #     if rec != None:
        #         context['image']=rec.MainImageFile
        # else:
        context['showTask']=True
        userId=self.request.session.get('user',None)['id']
        context['task_id'] = task_id
        context['user_id']=userId
        context['tasks'] = Tasks.objects.filter(CreateByUserId_id=userId)
        return context