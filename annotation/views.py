from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
#For celery
from annotation.tasks import sample_task
import json
from annotation.models import LineAnnotation, WordAnnotation

# Create your views here.
def celery_demo(request):
    
    print("celery begin")
    # example function
    sample_task.delay(
            "email", "message"
        )
    print("ok")

    return redirect('/annotate/main')

def save_lineAnnotateData(request):
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
            newLA.dict_id = d['dick_id']
            newLA.task_id = d['task_id']
            newLA.box_coordinates = d['box_coordinates']
            newLA.save()
        msg = True
        return JsonResponse({"msg": msg}, status=200)
        

def save_wordAnnotateData(request):
    if request.method == "POST" and request.is_ajax():
        data = request.POST.get('sendData')
        data = json.loads(data)

        for d in data:
            newWA = WordAnnotation()
            newWA.word_index = d['word_index']
            newWA.text = d['text']
            # newWA.is_fixed_text = d['is_fixed_text']
            # newWA.is_render_text = d['is_render_text']
            newWA.lang_id = d['lang_id']
            newWA.font_id = d['font_id']
            newWA.task_id = d['task_id']
            newWA.box_coordinates = d['box_coordinates']
            newWA.save()
        msg = True
        return JsonResponse({"msg": msg}, status=200)
        