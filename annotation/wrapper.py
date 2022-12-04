from annotation.models import LineAnnotation, WordAnnotation
from tools.utilities.box_helper import convert_annotation_boxes_str_2_list
from tools.utilities.word_grouping_helper import group_word_annotations_by_line

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

    from IPython import embed;embed()
