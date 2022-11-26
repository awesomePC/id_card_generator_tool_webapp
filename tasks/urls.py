from django.urls import path
from django.conf import settings
from tasks.add.views import ProjectAddView
from tasks.list.views import ProjectListView

app_name = 'tasks'

urlpatterns = [
    path('list', ProjectListView.as_view(template_name = 'pages/tasks/index.html'), name='list-tasks'),
    path('add-edit', ProjectAddView.as_view(template_name = 'pages/tasks/add-edit.html'), name='add-edit-tasks'),
]