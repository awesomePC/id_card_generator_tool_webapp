from django.urls import path
from django.conf import settings
from django.http import JsonResponse
from annotation import views
from annotation.main.views import AnnotateMainView
from annotation.wordlevel.views import AnnotateWordLevelView
from annotation.preview.views import AnnotatePreviewView
app_name = 'annotate'

urlpatterns = [
    path('main', AnnotateMainView.as_view(template_name = 'pages/annotate/index.html'), name='annotate-main'),
    path('wordlevel', AnnotateWordLevelView.as_view(template_name = 'pages/annotate/wordlevel.html'), name='annotate-wordlevel'),
    path('preview', AnnotatePreviewView.as_view(template_name = 'pages/annotate/preview.html'), name='annotate-preview'),
    path('celery-demo', views.celery_demo, name='annotate-celery'),
    path('save-lineannotate-data', views.save_lineAnnotateData, name='save-lineannodata'),
    path('save-wordannotate-data', views.save_wordAnnotateData, name='save-wordannodata'),
]