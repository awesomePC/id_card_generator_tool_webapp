from django.urls import path
from django.conf import settings
from annotation.main.views import AnnotateMainView
from tasks.models import Tasks
from django.http import JsonResponse

app_name = 'annotate'

urlpatterns = [
    path('main', AnnotateMainView.as_view(template_name = 'pages/annotate/index.html'), name='annotate-main'),
]