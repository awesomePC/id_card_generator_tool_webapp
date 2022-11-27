from django.urls import path
from django.conf import settings
from projects.addproject.views import ProjectAddView
from projects.listproj.views import ProjectListView
from projects.models import Projects
from django.http import JsonResponse

app_name = 'projects'

def duplicate_check(request):
    pid=int('0'+request.GET.get('id',None))
    name=request.GET.get('name',None)
    if pid != None and pid>0:
        exists=Projects.objects.filter(Name=name).exclude(id = pid).exists()
        return JsonResponse({'isDuplicate':exists})
    else:
        exists=Projects.objects.filter(Name=name).exists()
        return JsonResponse({'isDuplicate':exists})

urlpatterns = [
    path('list', ProjectListView.as_view(template_name = 'pages/projects/index.html'), name='list-project'),
    path('add-edit', ProjectAddView.as_view(template_name = 'pages/projects/add-edit.html'), name='add-edit-project'),
    path('duplicate',duplicate_check,name="projduplicatechk")
]