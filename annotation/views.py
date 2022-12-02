from django.shortcuts import render
from django.shortcuts import redirect
#For celery
from annotation.tasks import sample_task

# Create your views here.
def celery_demo(request):
    
    print("celery begin")
    # example function
    sample_task.delay(
            "email", "message"
        )
    print("ok")

    return redirect('/annotate/main')