import os
import numpy as np
import cv2
import imutils
from PIL import Image, ImageDraw, ImageFont
import gdown
from loguru import logger

def read_image(image_path, skew_correction=False, max_width = None, return_rgb=True):
    image_bgr = cv2.imread(image_path) 

    if skew_correction:
        from deskew import determine_skew
        # Correct skew
        grayscale = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)
        angle = determine_skew(grayscale)
        logger.debug(f"angle: {angle}")
        if angle:
            image_bgr = imutils.rotate_bound(image_bgr, angle)

    if max_width:
        height, width, channels = image_bgr.shape
        logger.debug(f"height: {height}, width: {width}, channels:{channels}")

        if width > max_width:
            image_bgr = imutils.resize(image_bgr, width=max_width)  ## inter=cv2.INTER_LANCZOS4

            height, width, channels = image_bgr.shape
            logger.debug(f"New height: {height}, New width: {width}")

    if return_rgb:
        ## Convert to RGB
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)
        return image_rgb
    else:
        return image_bgr

def draw_boxes(image, bounds, color='lime', width=2, text_font_size=14, text_fill_color="orange"):
    """
    Draw bounding boxes
    PIL text visualization util
    Args:
        image (pil): PIl image
        bounds (polypoints|rect): Text detection bounding boxes
        color (str, optional): Text highlighting color. Defaults to 'yellow'.
        width (int, optional): Border width. Defaults to 2.
    Returns:
        pil: text highlighted image
    """
    font_file = './fonts/Verdana.ttf'
    if not os.path.exists("./fonts"):
        os.makedirs("fonts", exist_ok=True)
        url = 'https://drive.google.com/uc?id=1a4Jyh3bwe6v6Hji1WaGgH-7nwA1YOHXb'
        
        gdown.download(url, font_file, quiet=False)

    font = ImageFont.truetype(font_file, text_font_size)
    
    draw = ImageDraw.Draw(image)
    for idx, bound in enumerate(bounds):
        # logger.debug(bound)
        if len(np.array(bound).shape) == 1: 
            ## rectangle
            xmin, xmax, ymin, ymax = bound
            draw.rectangle([xmin, ymin, xmax, ymax], outline=color, width=width)
        else:
            # Polygon
            p0, p1, p2, p3 = bound
            draw.line([*p0, *p1, *p2, *p3, *p0], fill=color, width=width)

            text = f"{idx}"
            draw.text(p0, text, font=font, align ="left", fill=text_fill_color) 
    return image


def clean_text(text, lower=True, remove_dot=True):
    """
    Remove whitespaces(right, lift, middle of text etc.), remove newsline
    Ocr results will be cleaned and then matched
    paddleocr will not detect space properly -- so it's necessary to remove intermediate spaces of tesserocr result to match it with paddleocr
    Args:
        text (str): OCR detected text
        lower (bool, optional): Whether to make text lowercase. Defaults to True.
        remove_dot (bool, optional): Remove dot from text. Defaults to True.
    Returns:
        str: Manipulated(cleaned) string
    """
    ## Remove whitespace, newline, tab, return key from text and then match
    text = text.translate(str.maketrans('', '', ' \n\t\r'))

    if lower:
        text = text.lower()
    
    if remove_dot:
        text = text.replace('.', '')

    return text

def sorted_boxes(dt_boxes, extra_box_sorting=True):
    """
    Sort text boxes in order from top to bottom, left to right
    args:
        dt_boxes(array):detected text boxes with shape [4, 2]
    return:
        sorted boxes(array) with shape [4, 2]
    """
    num_boxes = dt_boxes.shape[0]
    sorted_boxes = sorted(dt_boxes, key=lambda x: (x[0][1], x[0][0]))
    _boxes = list(sorted_boxes)

    ## If text detector paddleocr -- apply default extra_box_sorting
    if extra_box_sorting:
        for i in range(num_boxes - 1):
            if abs(_boxes[i + 1][0][1] - _boxes[i][0][1]) < 10 and \
                    (_boxes[i + 1][0][0] < _boxes[i][0][0]):
                tmp = _boxes[i]
                _boxes[i] = _boxes[i + 1]
                _boxes[i + 1] = tmp
    return _boxes

def contains_blue(img, is_rgb_input=True):
    """
    Check is image contains blue color
    """
    if is_rgb_input:
      img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
      
    # Convert the image to HSV colour space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Define a range for blue color
    hsv_l = np.array([100, 150, 0])
    hsv_h = np.array([140, 255, 255])

    # Find blue pixels in the image
    #
    # cv2.inRange will create a mask (binary array) where the 1 values
    # are blue pixels and 0 values are any other colour out of the blue
    # range defined by hsv_l and hsv_h
    return np.any(cv2.inRange(hsv, hsv_l, hsv_h))

def np_encoder(object):
    if isinstance(object, (np.generic, np.ndarray)):
        return object.tolist()