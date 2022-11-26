from django.views.generic import TemplateView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from ..models import Tasks
from projects.models import Projects
from django.shortcuts import redirect
from datetime import date

"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to urls.py file for more pages.
"""

class TasksAddView(TemplateView):
    template_name = 'pages/Tasks/add-edit.html'
    def dispatch(self, request, *args, **kwargs):
        if request.session.get('isAuthenticated',False) is False:
            return redirect('/signin')
        else:
            if request.method == 'POST':
                userid=request.session.get('user')['id']
                id=request.POST['id']
                name=request.POST['name']
                projectId=request.POST['projectId']
                if id != None and int('0'+id)>0:
                    rec=Tasks.objects.get(id=id)
                    rec.TaskName=name
                    rec.UpdatedDate=date.today()
                    rec.UpdatedByUserId_id=userid
                    rec.save()
                else:
                    proj=Tasks(TaskName=name,ProjectId_id=project_id,CreateByUserId_id=userid,UpdatedByUserId_id=userid)
                    proj.save()
                return redirect('/tasks/list')
            else:
                return super(TasksAddView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)
        # KTTheme.addJavascriptFile('js/custom/authentication/reset-password/new-password.js')
        id=self.request.GET.get('id',0).__str__()
        if id != None and int('0' + id) > 0:
            context['id']=id
            rec=Tasks.objects.filter(id=id).first()
            context['name']=rec.Name
        userid=self.request.session.get('user')['id']
        context['projects']=Projects.objects.filter(CreateByUserId_id=userid)
        return context
