from django.urls import path
from django.conf import settings
from tasks.add.views import TasksAddView
from tasks.list.views import TasksListView
from tasks.models import Tasks
from django.http import JsonResponse

app_name = 'tasks'
def duplicate_check(request):
    pid=int('0'+request.GET.get('id',None))
    name=request.GET.get('name',None)
    proj=request.GET.get('proj',None)
    if pid != None and pid>0:
        exists=Tasks.objects.filter(TaskName=name,ProjectId_id=proj).exclude(id = pid).exists()
        return JsonResponse({'isDuplicate':exists})
    else:
        exists=Tasks.objects.filter(TaskName=name,ProjectId_id=proj).exists()
        return JsonResponse({'isDuplicate':exists})
urlpatterns = [
    path('list', TasksListView.as_view(template_name = 'pages/tasks/index.html'), name='list-tasks'),
    path('add-edit', TasksAddView.as_view(template_name = 'pages/tasks/add-edit.html'), name='add-edit-tasks'),
    path('duplicate',duplicate_check,name="taskduplicatechk")
]