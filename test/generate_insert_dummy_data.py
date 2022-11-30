from django.conf import settings

import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 

## import django settings
from _keenthemes import settings as app_settings
settings.configure(INSTALLED_APPS=app_settings.INSTALLED_APPS,DATABASES=app_settings.DATABASES)

## setup django
import django
django.setup()

### some settings
MEDIA_ROOT = app_settings.MEDIA_ROOT

## Now you can access model
# from projects.models import Projects
# for s in Projects.objects.all():
#     print(s)

import shutil
from pathlib import Path

from auth.models import Users

## -----------------------------------------------------------------------------------------
## create dummy user
user, created = Users.objects.update_or_create(
    FirstName='TestUser', 
    LastName='Django',
    Email="TestUser@gmail.com",
    Password="TestUserDjango"
)

## -----------------------------------------------------------------------------------------
## Create dummy project
from projects.models import Projects
project, created_proj = Projects.objects.update_or_create(
    Name='TestProject', 
    CreateByUserId=user
)

### 
def copy_file_2_media_folder(input_file_path, sub_folder="dict"):
    """
    Copy file in media folder

    Args:
        input_file_path (_type_): _description_
        sub_folder (str, optional): _description_. Defaults to "dict".

    Returns:
        _type_: _description_
    """
    media_relative_path = os.path.join(sub_folder, Path(input_file_path).name)
    output_file_path = os.path.join(MEDIA_ROOT, media_relative_path)
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
    shutil.copy2(input_file_path, output_file_path)
    return media_relative_path


## -----------------------------------------------------------------------------------------
## Create dummy task
from tasks.models import Tasks

input_main_file_path = "./resources/images/task_main/main.png"
main_img_media_relative_path = copy_file_2_media_folder(input_main_file_path, "images")

input_cleaned_file_path = "./resources/images/task_main/cleaned.png"
cleaned_img_media_relative_path = copy_file_2_media_folder(input_cleaned_file_path, "images")

task, created_task = Tasks.objects.update_or_create(
    TaskName='TestTask', 
    ProjectId=project,
    CreateByUserId=user,
    MainImageFile=main_img_media_relative_path,
    TextRemovedImageFile=cleaned_img_media_relative_path,
)

## -----------------------------------------------------------------------------------------
## Generate dict object
from annotation.models import (
    DictionaryHub, LanguageHub, FontHub,
    LineAnnotation, WordAnnotation
)

input_file_path = "./resources/dict/english_person_name_cnt-50.txt"
dict_media_relative_path = copy_file_2_media_folder(input_file_path, "dict")

dictionary_obj , created_dict = DictionaryHub.objects.update_or_create(
    name='TestDictionary', 
    type="text",
    file=dict_media_relative_path,
    created_by_user=user
)

## -----------------------------------------------------------------------------------------
## create language
lang_obj , created_lang = LanguageHub.objects.update_or_create(
    name='TestEnglish', 
    short_name="en",
)

## -----------------------------------------------------------------------------------------
## create font dummy record
input_font_file_path = f"./resources/fonts/verdana.ttf"
font_media_relative_path = copy_file_2_media_folder(input_font_file_path, f"fonts/{lang_obj.name}")

font_obj , created_font = FontHub.objects.update_or_create(
    name='TestVerdana', 
    file=font_media_relative_path,
    lang=lang_obj
)

## After this from UI -- line and word level annotations will be created 
## But in dummy record generation we will take sample meta.json file
input_meta_file_path = "./resources/images/task_main/meta.json"
meta_json_media_relative_path = copy_file_2_media_folder(input_meta_file_path, "images")

task.meta_json_file = meta_json_media_relative_path
task.save()

## now reverse step -- manually generating LineAnnotation -- in dummy test from dummy meta.json
## read json
import json
with open(input_meta_file_path, encoding="utf-8") as json_file:
    meta_data = json.load(json_file)

## 
from image_cropping import read_image, crop_img_boxes, get_rotate_crop_image
from PIL import Image
import numpy as np
img = np.asarray(Image.open(input_main_file_path))


for i, box in enumerate(meta_data["boxes"]):
    # import ipdb;ipdb.set_trace()
    # cropped_images = crop_img_boxes(img, np.asarray([box["box_coordinates"]]), use_four_point_transform=True, use_angle_cls=False)
    cropped_images = get_rotate_crop_image(img, np.asarray(box["box_coordinates"]))
    cropped_image = cropped_images[0]
    pil_img = Image.fromarray(np.asarray(cropped_image))
    # img_path = f"cropped_line_imgs/task_{instance.task.id}/{filename}"
    cropped_img_path = f"./resources/images/{i}.png"
    pil_img.save(cropped_img_path)
    cropped_img_media_relative_path = copy_file_2_media_folder(cropped_img_path, f"task_{task.id}/{i}.png")

    line_anno_obj , created = LineAnnotation.objects.update_or_create(
        line_index=box["box_index"], 
        type=box["box_type"],
        box_coordinates=box["box_coordinates"],
        is_fixed_text = box["is_fixed_text"],
        is_render_text = box["is_render_text"],
        dict = box["dict_file_multi"],
        cropped_image=cropped_img_media_relative_path,
        task=task,
    )
# from IPython import embed; embed()