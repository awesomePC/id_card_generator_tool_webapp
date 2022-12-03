from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
#For celery
from annotation.tasks import sample_task
import json
from annotation.models import LineAnnotation

# Create your views here.
def celery_demo(request):
    
    print("celery begin")
    # example function
    sample_task.delay(
            "email", "message"
        )
    print("ok")

    return redirect('/annotate/main')

def send_data(request):
    if request.method == "POST" and request.is_ajax():
        data = request.POST.get('sendData')
        data = json.loads(data)

        for d in data:
            newLA = LineAnnotation()
            newLA.line_index = d['line_index']
            newLA.type = d['type']
            newLA.text = d['text']
            newLA.is_fixed_text = d['is_fixed_text']
            newLA.is_render_text = d['is_render_text']
            newLA.dict_id = 1
            print(d['dict_id'])
            newLA.task_id = 1
            print(d['task_id'])
            newLA.box_coordinates = d['box_coordinates']
            newLA.save()
        msg = True
        return JsonResponse({"msg": msg}, status=200)
        