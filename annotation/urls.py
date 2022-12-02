from django.urls import path
from django.conf import settings
from annotation.main.views import AnnotateMainView
from .wordlevel.views import AnnotateWordLevelView
from .GenratePenData.views import GenrateDataPenCard,VolumeAndComment
from tasks.models import Tasks
from django.http import JsonResponse

app_name = 'annotate'

urlpatterns = [
    path('main', AnnotateMainView.as_view(template_name = 'pages/annotate/index.html'), name='annotate-main'),
    path('wordlevel', AnnotateWordLevelView.as_view(template_name = 'pages/annotate/wordlevel.html'), name='annotate-wordlevel'),
    path('genratedatapencard', GenrateDataPenCard.as_view(template_name = 'pages/annotate/genratedatapencard.html'), name='genrate-data-pan-card'),
    path('volumeandcomment', VolumeAndComment.as_view(template_name = 'pages/annotate/volume_and_comment.html'), name='volume-and-comment'),
]