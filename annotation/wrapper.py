import os
from pathlib import Path
from django.http import JsonResponse
from annotation.models import LineAnnotation, WordAnnotation, LineAnnotationExtraInfo
from tools.utilities.box_helper import convert_annotation_boxes_str_2_list
from tools.utilities.word_grouping_helper import group_word_annotations_by_line
from nb_utils.dict_manipulation import get_multi_occurrence_key_value
from tools.utilities.nutility import draw_boxes

from tasks.models import Tasks
from annotation.models import LineAnnotation, WordAnnotation, LineAnnotationExtraInfo, AnnotationMetaInfo
from tools.utilities.box_helper import convert_annotation_boxes_str_2_list
from PIL import Image

from io import BytesIO
from django.core.files import File

def visualize_annotation(task_id, annotation_type="line", show_visualized_image=True):
    """
    Visualize line and word coordinates

    Args:
        task_id (_type_): _description_
    """
    if annotation_type == "line":
        line_annotations = LineAnnotation.objects.filter(task_id=task_id).defer(
            "created_at", "updated_at"
        ).values()

        line_annotations = convert_annotation_boxes_str_2_list(line_annotations)
        bb_boxes = get_multi_occurrence_key_value(list(line_annotations), "box_coordinates")
    else:
        word_annotations = WordAnnotation.objects.filter(task_id=task_id).values(
            "id", "box_coordinates"
        )
        word_annotations = convert_annotation_boxes_str_2_list(word_annotations)
        bb_boxes = get_multi_occurrence_key_value(list(word_annotations), "box_coordinates")

    ## get task object for getting name
    task = Tasks.objects.get(id=task_id)

    if bb_boxes:
        total_boxes = len(bb_boxes)
        image_filepath = task.MainImageFile.path

        image = Image.open(image_filepath)
        visualized_image = draw_boxes(image, bb_boxes, font_file="./assets/font/Verdana.ttf")

        if show_visualized_image:
            try:
                visualized_image.show()
            except Exception as e:
                print(f"Error in showing visualized image...")
                pass
        
        # from IPython import embed; embed()

        # save PIl image in django
        blob = BytesIO()
        visualized_image.save(blob, 'PNG')
        image_file_name = "visualized_" + Path(image_filepath).name

        meta_info, created = AnnotationMetaInfo.objects.get_or_create(task_id=task_id)
        if annotation_type == "line":
            meta_info.image_visualized_lines.save(image_file_name, File(blob), save=False)
        else:
            meta_info.image_visualized_words.save(image_file_name, File(blob), save=False)

        meta_info.save()

        return JsonResponse({
            "status": "Annotation successfully visualized .. and saved in db",
            "annotation_type": annotation_type,
            "task_name": task.TaskName,
            "output-table-name": "AnnotationMetaInfo",
            "output-id": meta_info.id
        })
    else:
        return JsonResponse({
            "status": "info.. skipping visualization.. no bounding boxes record available..",
            "annotation_type": annotation_type,
            "task_name": task.TaskName,
        })
        
def group_words_by_line_coordinates(task_id):
    """
    group words by line coordinates
    """
    line_annotations = LineAnnotation.objects.filter(task_id=task_id).defer(
        "created_at", "updated_at"
    ).values()

    word_annotations = WordAnnotation.objects.filter(task_id=task_id).values(
        "id", "word_index", "text", "lang", "font",
        "box_coordinates", "task"
    )

    # box_coordinates_str = line_annotations[0]["box_coordinates"]
    # ## convert string format coordinates back to list of lists
    # box_coordinates = json.loads(box_coordinates_str)

    line_annotations = convert_annotation_boxes_str_2_list(line_annotations)
    word_annotations = convert_annotation_boxes_str_2_list(word_annotations)

    grouped_words_annotation_by_line = group_word_annotations_by_line(
        line_annotations, word_annotations, sort=True
    )

    # update table
    for single_line_annotation in grouped_words_annotation_by_line:
        grouped_word_annotations = single_line_annotation["grouped_word_annotations"]
        if grouped_word_annotations:
            word_ids = get_multi_occurrence_key_value(grouped_word_annotations, key_name="id", log=False)

            # save line info
            obj_line_extra_info, created = LineAnnotationExtraInfo.objects.get_or_create(
                line_id=single_line_annotation["id"]
            )

            # words_obj = WordAnnotation.objects.filter(id__in=word_ids)

            # # Now saving the ManyToManyField
            # for word_id in word_ids:
            #     obj_line_extra_info.grouped_words_annotation_by_line.add(word_id)

            obj_line_extra_info.inside_words = ','.join([str(elem) for elem in word_ids])
            obj_line_extra_info.save()

    ## --------------------------------------------------------------
    ## visualize and save image
    ## for now simply drawing line and words annotation will be better to save time
    ## Later we can add separate color for each word group
    task = Tasks.objects.get(id=task_id)
    image_filepath = task.MainImageFile.path

    image = Image.open(image_filepath)

    # draw line boxes first
    bb_boxes = get_multi_occurrence_key_value(list(line_annotations), "box_coordinates")
    visualized_image = draw_boxes(
        image, bb_boxes, 
        color="orange",
        is_draw_sequence_number=False
    )

    ## draw word boxes on it
    word_bb_boxes = get_multi_occurrence_key_value(list(word_annotations), "box_coordinates")
    visualized_image = draw_boxes(
        visualized_image, word_bb_boxes,
        font_file="./assets/font/Verdana.ttf"
    )

    # save PIl image in django
    blob = BytesIO()
    visualized_image.save(blob, 'PNG')
    image_file_name = "visualized_grouped_words" + Path(image_filepath).name

    meta_info, created = AnnotationMetaInfo.objects.get_or_create(task_id=task_id)
    meta_info.image_visualized_grouped_words.save(image_file_name, File(blob), save=False)
    meta_info.save()

    ## visualization end--------------------------------------------------------------

    # from IPython import embed;embed()

    ## TODO: Add metadata file generator method
    return JsonResponse({
        "status": "Grouping word coordinates by line completed",
        "task_id": task_id,
    })