from django.urls import path
from django.conf import settings
from tasks.add.views import TasksAddView
from tasks.list.views import TasksListView

app_name = 'tasks'

urlpatterns = [
    path('list', TasksListView.as_view(template_name = 'pages/tasks/index.html'), name='list-tasks'),
    path('add-edit', TasksAddView.as_view(template_name = 'pages/tasks/add-edit.html'), name='add-edit-tasks'),
]