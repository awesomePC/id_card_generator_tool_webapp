from django.urls import path
from django.conf import settings
from tasks.models import Tasks
from django.http import JsonResponse
from dataset import views
from dataset.generate_dataset.views import GenerateData
from dataset.augment_dataset.views import AugmentData 
from dataset.paste_dataset.views import PasteData
from dataset.list_dataset.views import ListData
from dataset.view_dataset.views import ViewData
from dataset import views
app_name = 'dataset'

urlpatterns = [
    path('generate_dataset', GenerateData.as_view(template_name = 'pages/dataset/generate_dataset.html'), name='generate_dataset'),
    path('paste_dataset', PasteData.as_view(template_name = 'pages/dataset/paste_dataset.html'), name='paste_dataset'),
    path('augment_dataset', AugmentData.as_view(template_name = 'pages/dataset/augment_dataset.html'), name='augment_dataset'),
    path('list_dataset', ListData.as_view(template_name = 'pages/dataset/list_dataset.html'), name='list_dataset'),
    path('view_dataset/<int:id>', ViewData.as_view(template_name = 'pages/dataset/view_dataset.html'), name='view_dataset'),
    
]