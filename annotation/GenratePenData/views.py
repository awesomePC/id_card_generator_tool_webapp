from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from tasks.models import Tasks
from annotation.models import GenratePanData,VolumeComment
from django.shortcuts import redirect
from django.shortcuts import render


"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""
class GenrateDataPenCard(TemplateView):
    template_name = 'pages/annotate/genratedatapencard.html'
    
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('isAuthenticated',False) is False:
            return redirect('/signin')
        else:
            if request.method == 'POST':
                set_data = request.POST["data_set"]
                set_count = request.POST["data_count"]
                selct_task = request.POST["select_task"]
                description = request.POST["description"]
                genrate_data = GenratePanData(set_data = set_data,count = set_count,select_task_id= selct_task,description = description)
                genrate_data.save()
                return redirect('annotate:genrate-data-pan-card')
            else:
                return super(GenrateDataPenCard, self).get(request, *args, **kwargs)
                    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Call the base implementation first to get a context
        context = KTLayout.init(context)
        userId=self.request.session.get('user',None)['id']
        context['tasks'] = Tasks.objects.filter(CreateByUserId_id=userId)
        return context


class VolumeAndComment(TemplateView):
    template_name = 'pages/annotate/volume_and_comment.html'
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('isAuthenticated',False) is False:
            return redirect('/signin')
        else:
            if request.method == 'POST':
                set_data = request.POST["data_set"]
                set_count = request.POST["data_count"]
                selct_task = request.POST["select_task"]
                description = request.POST["description"]
                genrate_data = VolumeComment(set_data = set_data,count = set_count,select_task_id= selct_task,description = description)
                genrate_data.save()
                return redirect('annotate:volume-and-comment')
            else:
                return super(VolumeAndComment, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Call the base implementation first to get a context
        context = KTLayout.init(context)
        userId=self.request.session.get('user',None)['id']
        context['tasks'] = Tasks.objects.filter(CreateByUserId_id=userId)
        return context
