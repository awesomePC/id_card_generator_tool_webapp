from django.urls import path
from django.conf import settings
from tasks.models import Tasks
from django.http import JsonResponse
from dataset import views
from dataset.generate_dataset.views import GenerateData
app_name = 'dataset'

urlpatterns = [
    path('generate_dataset', GenerateData.as_view(template_name = 'pages/dataset/generate_dataset.html'), name='generate_dataset'),
    path('paste_dataset', GenerateData.as_view(template_name = 'pages/dataset/paste_dataset.html'), name='paste_dataset'),
    path('argument_dataset', GenerateData.as_view(template_name = 'pages/dataset/argument_dataset.html'), name='argument_dataset'),
    path('list_dataset', GenerateData.as_view(template_name = 'pages/dataset/generate_dataset.html'), name='list_dataset'),
    path('view_dataset/<int:id>', GenerateData.as_view(template_name = 'pages/dataset/generate_dataset.html'), name='view_dataset'),
]