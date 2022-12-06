from django.shortcuts import render
from django.shortcuts import redirect
from django.http import JsonResponse
#For celery
from annotation.tasks import sample_task
import json
from annotation.models import LineAnnotation, WordAnnotation
from django.db.models import Max

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
        
        # import ipdb; ipdb.set_trace()

        # getting max line_index
        LAs = LineAnnotation.objects.filter(task_id = data[0]['task_id'])
        if LAs.exists():
            max_lineIndex = LAs.order_by('-line_index')[0].line_index
        else:
            max_lineIndex = 0
      
        for d in data:
            newLA = LineAnnotation()
            newLA.line_index = max_lineIndex + d['line_index']
            newLA.type = d['type']
            newLA.text = d['text']
            newLA.is_fixed_text = d['is_fixed_text']
            newLA.is_render_text = d['is_render_text']
            newLA.dict_id = d['dict_id']
            newLA.task_id = d['task_id']
            newLA.key_label = d['key_label']
            newLA.box_coordinates = d['box_coordinates']
            newLA.save()
        msg = True
        return JsonResponse({"msg": msg}, status=200)
        

def save_wordAnnotateData(request):
    if request.method == "POST" and request.is_ajax():
        data = request.POST.get('sendData')
        data = json.loads(data)

        # getting max word_index
        WAs = WordAnnotation.objects.filter(task_id = data[0]['task_id'])
        if WAs.exists():
            max_wordIndex = WAs.order_by('-word_index')[0].word_index
        else:
            max_wordIndex = 0

        for d in data:
            newWA = WordAnnotation()
            newWA.word_index = max_wordIndex + d['word_index']
            newWA.text = d['text']
            newWA.is_bold = d['is_bold']
            newWA.is_italic = d['is_italic']
            newWA.lang_id = d['lang_id']
            newWA.font_id = d['font_id']
            newWA.task_id = d['task_id']
            newWA.box_coordinates = d['box_coordinates']
            newWA.save()
        msg = True
        return JsonResponse({"msg": msg}, status=200)

def view_visualize_line_annotation(request, task_id):
    """
    Visualize line coordinates

    Args:
        request (_type_): _description_
        task_id (_type_): _description_
    """
    from annotation.wrapper import visualize_annotation
    json_response = visualize_annotation(
        task_id, 
        annotation_type="line",
        show_visualized_image=True
    )
    return json_response

def view_visualize_word_annotation(request, task_id):
    """
    Visualize word coordinates

    Args:
        request (_type_): _description_
        task_id (_type_): _description_
    """
    from annotation.wrapper import visualize_annotation
    json_response = visualize_annotation(
        task_id, 
        annotation_type="word",
        show_visualized_image=True
    )
    return json_response