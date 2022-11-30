#@title utils for image cropping based on text coordinates 
import copy
import cv2
import numpy as np
import imutils
from imutils.perspective import four_point_transform


def get_rotate_crop_image(img, points):
    '''
    img_height, img_width = img.shape[0:2]
    left = int(np.min(points[:, 0]))
    right = int(np.max(points[:, 0]))
    top = int(np.min(points[:, 1]))
    bottom = int(np.max(points[:, 1]))
    img_crop = img[top:bottom, left:right, :].copy()
    points[:, 0] = points[:, 0] - left
    points[:, 1] = points[:, 1] - top
    '''
    img_crop_width = int(
        max(
            np.linalg.norm(points[0] - points[1]),
            np.linalg.norm(points[2] - points[3])))
    img_crop_height = int(
        max(
            np.linalg.norm(points[0] - points[3]),
            np.linalg.norm(points[1] - points[2])))
    pts_std = np.float32([[0, 0], [img_crop_width, 0],
                          [img_crop_width, img_crop_height],
                          [0, img_crop_height]])
    M = cv2.getPerspectiveTransform(points, pts_std)
    dst_img = cv2.warpPerspective(
        img,
        M, (img_crop_width, img_crop_height),
        borderMode=cv2.BORDER_REPLICATE,
        flags=cv2.INTER_CUBIC)
    # dst_img_height, dst_img_width = dst_img.shape[0:2]
    # if dst_img_height * 1.0 / dst_img_width >= 1.5:
    #     dst_img = np.rot90(dst_img)
    return dst_img


def check_vertical_image(img_crop):
    """
    If vertical image rotate 90 degree clockwise
    """
    height, width, channel = img_crop.shape

    ## (width * 1.5) instead of just width to avoid rotation on single character
    if height > (width * 1.3):
        try:
            # print("line image height greater than width: Rotating word -- clockwise 90 degree")
            img_crop = imutils.rotate_bound(img_crop, angle=90) # rotate word if vertical
            # height, width = width, height # swap values
        except Exception as e:
            pass
    return img_crop
                    

def crop_img_boxes(img, dt_boxes, rotate_vertical=True, use_angle_cls=True, use_four_point_transform=False, obj_paddleocr_text_classifier=None):

    img_crop_list = list()
    angle_list = []
    # print(type(img_crop_list))

    for bno in range(len(dt_boxes)):
        tmp_box = copy.deepcopy(dt_boxes[bno])
        # print(tmp_box)
        # print(np.array(tmp_box).shape)
        # print(len(np.array(tmp_box).shape))

        if len(np.array(tmp_box).shape) == 1: 
            ## rectangle
            x1, x2, y1, y2 = tmp_box
            img_crop = img[y1:y2, x1:x2] # .copy()
            # print(img_crop.shape)
            
            if rotate_vertical:
                img_crop = check_vertical_image(img_crop)

            img_crop_list.append(img_crop)
            # print(type(img_crop_list[0]))
        else:
            if use_four_point_transform:
                img_crop = four_point_transform(img, tmp_box)
            else:
                img_crop = get_rotate_crop_image(img, tmp_box)

            if rotate_vertical:
                ## check is vertical image -- if vertical image rotate 90 degree
                img_crop = check_vertical_image(img_crop)

            img_crop_list.append(img_crop)

    if use_angle_cls:
        # img_crop_list, angle_list, elapse = paddleocr_engine.text_classifier(
        #     img_crop_list
        # )
        
        if obj_paddleocr_text_classifier:
            img_crop_list, angle_list, elapse = obj_paddleocr_text_classifier(
                img_crop_list
            )
            print("cls num  : {}, elapse : {}".format(
                len(img_crop_list), elapse))
        else:
            print(f"Warning... obj_paddleocr_text_classifier not set.. skipping angle classification")
        
    return img_crop_list, angle_list


# ---------------------------------------------------
import os
import numpy as np
import cv2
import imutils
from PIL import Image, ImageDraw, ImageFont
import gdown


def read_image(image_path, skew_correction=False, max_width = None, return_rgb=True):
    image_bgr = cv2.imread(image_path) 

    if skew_correction:
        from deskew import determine_skew
        # Correct skew
        grayscale = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        angle = determine_skew(grayscale)
        print(f"angle: {angle}")
        if angle:
            image_bgr = imutils.rotate_bound(image_bgr, angle)

    if max_width:
        height, width, channels = image_bgr.shape
        print(f"height: {height}, width: {width}, channels:{channels}")

        if width > max_width:
            image_bgr = imutils.resize(image_bgr, width=max_width)  ## inter=cv2.INTER_LANCZOS4

            height, width, channels = image_bgr.shape
            print(f"New height: {height}, New width: {width}")

    if return_rgb:
        ## Convert to RGB
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        return image_rgb
    else:
        return image_bgr