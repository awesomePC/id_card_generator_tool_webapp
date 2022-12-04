import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
from loguru import logger

def group_word_annotations_by_line(line_annotations, word_annotations, sort=True):
    """
    Group words of annotations by line annotations

    Args:
        line_annotations (list): list of dicts containing line level annotation, and contains box coordinates for each line
        word_annotations (list): list of dicts containing line level annotation, and contains box coordinates for each line
        sort (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    for loop_index, line_annotation in enumerate(line_annotations):
        box_2d_poly = line_annotation["box_coordinates"]
        polygon = Polygon(np.squeeze(box_2d_poly))
        
        ## list all words of single line
        all_words_annotation_single_line = []
        for word_annotation in word_annotations:
            word_points = word_annotation["box_coordinates"]
            centroid = Polygon(word_points).centroid
            point = Point(centroid)

            is_inside = polygon.contains(point)
            # logger.debug(f"Is contains: {is_inside}")

            if is_inside:
                all_words_annotation_single_line.append(word_annotation)

        if all_words_annotation_single_line:
            ## Sort words of line from left to right
            if sort:
                ## Sorting
                sorted_boxes = sorted(
                    np.array(all_words_annotation_single_line), 
                    key=lambda x: x["box_coordinates"][0][0]
                )
                all_words_annotation_single_line = list(sorted_boxes)

        ## for each line -- group the words -- add new key
        line_annotations[loop_index]["grouped_word_annotations"] = all_words_annotation_single_line

    return line_annotations


def group_words_by_line(dt_boxes_lines, dt_boxes_words):
    """
    Group words by line

    Args:
        dt_boxes_lines (list): Line level boxes only
        dt_boxes_words (list): Word level boxes only

    Returns:
        list: list of lists
    """
    grouped_words_boxes = []
    for box_2d_poly in dt_boxes_lines:
        polygon = Polygon(np.squeeze(box_2d_poly))

        line_words_boxes = []
        for word_points in dt_boxes_words:
            # import ipdb; ipdb.set_trace()
            centroid = Polygon(word_points).centroid # word_points.mean(axis=0)
            # logger.debug(f"centroid: {centroid}")

            # point = Point(0.5, 0.5)
            # polygon = Polygon([(0, 0), (0, 1), (1, 1), (1, 0)])

            point = Point(centroid)
            
            is_inside = polygon.contains(point)
            # logger.debug(f"Is contains: {is_inside}")

            if is_inside:
                line_words_boxes.append(word_points)

        ## Sort words of line from left to right
        if line_words_boxes:
            ## Sorting
            sorted_boxes = sorted(np.array(line_words_boxes), key=lambda x: x[0][0])
            _boxes = list(sorted_boxes)

            grouped_words_boxes.append(
                _boxes
            )
        else:
            grouped_words_boxes.append([])
            pass
    return grouped_words_boxes

