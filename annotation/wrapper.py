from annotation.models import LineAnnotation, WordAnnotation, LineAnnotationExtraInfo
from tools.utilities.box_helper import convert_annotation_boxes_str_2_list
from tools.utilities.word_grouping_helper import group_word_annotations_by_line
from nb_utils.dict_manipulation import get_multi_occurrence_key_value

def group_words_by_line_coordinates(task_id):
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
            obj_line_extra_info = LineAnnotationExtraInfo.objects.create(line_id=single_line_annotation["id"])

            # words_obj = WordAnnotation.objects.filter(id__in=word_ids)

            # Now saving the ManyToManyField
            for word_id in word_ids:
                obj_line_extra_info.grouped_words_annotation_by_line.add(word_id)

    # from IPython import embed;embed()
    # pass

    ## TODO: Add metadata file generator method
    return True
