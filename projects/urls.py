from django.urls import path
from django.conf import settings
from projects.addproject.views import ProjectAddView
from projects.listproj.views import ProjectListView

app_name = 'projects'

urlpatterns = [
    path('list', ProjectListView.as_view(template_name = 'pages/projects/index.html'), name='list-project'),
    path('add-edit', ProjectAddView.as_view(template_name = 'pages/projects/add-edit.html'), name='add-edit-project'),
]