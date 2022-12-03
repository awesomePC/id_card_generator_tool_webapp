from django.urls import path
from django.conf import settings
from annotation.main.views import AnnotateMainView
from .wordlevel.views import AnnotateWordLevelView
<<<<<<< HEAD
from .preview.views import AnnotatePreviewView
=======
from .GenratePenData.views import GenrateDataPenCard,VolumeAndComment
>>>>>>> origin/Kuldeep
from tasks.models import Tasks
from django.http import JsonResponse
from annotation import views
app_name = 'annotate'

urlpatterns = [
    path('main', AnnotateMainView.as_view(template_name = 'pages/annotate/index.html'), name='annotate-main'),
    path('wordlevel', AnnotateWordLevelView.as_view(template_name = 'pages/annotate/wordlevel.html'), name='annotate-wordlevel'),
<<<<<<< HEAD
    path('preview', AnnotatePreviewView.as_view(template_name = 'pages/annotate/preview.html'), name='annotate-preview'),
    path('celery-demo', views.celery_demo, name='annotate-celery'),
    path('save-lineannotate-data', views.save_lineAnnotateData, name='save-lineannodata'),
    path('save-wordannotate-data', views.save_wordAnnotateData, name='save-wordannodata'),
    
=======
    path('genratedatapencard', GenrateDataPenCard.as_view(template_name = 'pages/annotate/genratedatapencard.html'), name='genrate-data-pan-card'),
    path('volumeandcomment', VolumeAndComment.as_view(template_name = 'pages/annotate/volume_and_comment.html'), name='volume-and-comment'),
>>>>>>> origin/Kuldeep
]