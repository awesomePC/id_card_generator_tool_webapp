import json

def convert_annotation_boxes_str_2_list(annotations, box_key_name="box_coordinates"):
    """
    convert string format box coordinates of annotation dict to list format

    Args:
        annotations (list): list of dicts
        box_key_name (str, optional): _description_. Defaults to "box_coordinates".

    Returns:
        list: list of dicts with modified datatype of box coordinates
    """
    for i in range(0, len(annotations)):
        if isinstance(annotations[i][box_key_name], str):
            annotations[i][box_key_name] = json.loads(annotations[i][box_key_name])
    return annotations