from django.urls import path
from django.conf import settings
from annotation.main.views import AnnotateMainView
from .wordlevel.views import AnnotateWordLevelView
from .preview.views import AnnotatePreviewView
from tasks.models import Tasks
from django.http import JsonResponse
from annotation import views
app_name = 'annotate'

urlpatterns = [
    path('main', AnnotateMainView.as_view(template_name = 'pages/annotate/index.html'), name='annotate-main'),
    path('wordlevel', AnnotateWordLevelView.as_view(template_name = 'pages/annotate/wordlevel.html'), name='annotate-wordlevel'),
    path('preview', AnnotatePreviewView.as_view(template_name = 'pages/annotate/preview.html'), name='annotate-preview'),
    path('celery-demo', views.celery_demo, name='annotate-celery'),
    path('send-data', views.send_data, name='send_data'),
    
]