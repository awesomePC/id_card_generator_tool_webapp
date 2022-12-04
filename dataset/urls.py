from django.urls import path
from django.conf import settings
from tasks.models import Tasks
from django.http import JsonResponse
from dataset import views
from dataset.generate_dataset.views import GenerateData
app_name = 'dataset'

urlpatterns = [
    path('generate_dataset', GenerateData.as_view(template_name = 'pages/dataset/generate_dataset.html'), name='generate_dataset'),
]