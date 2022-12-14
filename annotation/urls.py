from django.urls import path
from django.conf import settings
from django.http import JsonResponse
from annotation import views
from annotation.main.views import AnnotateMainView
from annotation.wordlevel.views import AnnotateWordLevelView
from annotation.preview.views import (
    AnnotatePreviewView
)
app_name = 'annotate'

urlpatterns = [
    path('main/<int:id>', AnnotateMainView.as_view(template_name = 'pages/annotate/index.html'), name='annotate-main'),
    path('wordlevel/<int:id>', AnnotateWordLevelView.as_view(template_name = 'pages/annotate/wordlevel.html'), name='annotate-wordlevel'),
    path('preview', AnnotatePreviewView.as_view(template_name = 'pages/annotate/preview.html'), name='annotate-preview'),
    path('celery-demo', views.celery_demo, name='annotate-celery'),
    path('save-lineannotate-data', views.save_lineAnnotateData, name='save-lineannodata'),
    path('save-wordannotate-data', views.save_wordAnnotateData, name='save-wordannodata'),

    path('visualize_line_annotation/<int:task_id>', views.view_visualize_line_annotation, name='view_visualize_line_annotation'),
    path('visualize_word_annotation/<int:task_id>', views.view_visualize_word_annotation, name='view_visualize_word_annotation'),
    path('group_words_by_line_coordinates/<int:task_id>', views.view_group_words_by_line_coordinates, name='group_words_by_line_coordinates'),
]