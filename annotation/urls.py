from django.urls import path
from django.conf import settings
from annotation.main.views import AnnotateMainView
from .wordlevel.views import AnnotateWordLevelView
from .preview.views import AnnotatePreviewView
from .GenratePenData.views import GenrateDataPenCard,VolumeAndComment
from tasks.models import Tasks
from django.http import JsonResponse
from annotation import views
app_name = 'annotate'

urlpatterns = [
    path('main/<int:id>', AnnotateMainView.as_view(template_name = 'pages/annotate/index.html'), name='annotate-main'),
    path('wordlevel', AnnotateWordLevelView.as_view(template_name = 'pages/annotate/wordlevel.html'), name='annotate-wordlevel'),
    path('preview', AnnotatePreviewView.as_view(template_name = 'pages/annotate/preview.html'), name='annotate-preview'),
    path('celery-demo', views.celery_demo, name='annotate-celery'),
    path('save-lineannotate-data', views.save_lineAnnotateData, name='save-lineannotate-data'),
    path('save-wordannotate-data', views.save_wordAnnotateData, name='save-wordannotate-data'),
    
    path('genratedatapencard', GenrateDataPenCard.as_view(template_name = 'pages/annotate/genratedatapencard.html'), name='genrate-data-pan-card'),
    path('volumeandcomment', VolumeAndComment.as_view(template_name = 'pages/annotate/volume_and_comment.html'), name='volume-and-comment'),
]