from django.db import models
from auth.models import Users
from annotation.choices import CONTENT_TYPE_CHOICES, TEXT_CASE_CHOICES
from tasks.models import Tasks

# Create your models here.

class DictionaryHub(models.Model):
    """
    Collection of dictionaries -- from this the ID card generator will take text to render on new image

    Model to store all dictionaries 

    Text dictionary : Words of text lines separated by newline
    Image dictionary: Store the path of images ex. face images or logo images path
    Args:
        models (_type_): _description_
    """
    name = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="name of dictionary ex. indian_person_names_english_cnt_1000",
    )
    type = models.CharField(
        max_length=5,
        choices=CONTENT_TYPE_CHOICES,
        help_text="type of content 1) text -- means words or lines text 2) image: path of images"
    )
    file = models.FileField(upload_to="dict/")
    desc = models.TextField(
        blank=True, null=True,
        help_text="Description of Dictionary"
    )
    desc_html = models.TextField(
        blank=True, null=True,
        help_text="Description of Dictionary in html format"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey(
        Users, related_name='createdByUser', blank=True, null=True, on_delete=models.CASCADE
    )
    updated_by_user = models.ForeignKey(
        Users, related_name='updatedByUser', blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name 

def cropped_line_image_path(instance, filename):
    """
    Custom path to upload cropped line images part
    """
    return f"cropped_line_imgs/task_{instance.task.id}/{filename}"


class LineAnnotation(models.Model):
    """
    Line annotations of each task on main image

    Note:
    In rendering preview - point 7, after resizing line annotations will be updated and again new cropped parts will be stored
    
    TODO:
        1) If image bounding box add option to specify margin, blending options etc..
        2) In rendering preview:
          - We can add shadow and check in realtime
          - change font in realtime
          - change text spacing and other properties
    """
    line_index = models.IntegerField(
        blank=True, null=True,
        help_text="Line index in image"
    )
    type = models.CharField(
        max_length=5,
        choices=CONTENT_TYPE_CHOICES,
        help_text="type of bounding box -- what bounding box holding 1) text 2) image"
    )
    text = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="text if content type is `text`",
    )
    is_fixed_text = models.BooleanField(default=False)
    is_render_text = models.BooleanField(default=True)
    box_coordinates = models.TextField(
        null=True, blank=True,
        help_text="Bounding box coordinates. TODO. use ArrayField or JSONfield later"
    )
    key_label = models.CharField(
        max_length=255, null=True, blank=True,
        default="OTHER",
        help_text="Key name for structured data training purpose ex. PERSON_NAME, BIRTH_DATE etc.."
    )
    task = models.ForeignKey(
        Tasks, blank=True, on_delete=models.CASCADE,
        help_text="Task id in which this line annotation belongs"
    )
    dict = models.ForeignKey(DictionaryHub, blank=True, on_delete=models.CASCADE)
    cropped_image = models.ImageField(upload_to=cropped_line_image_path, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task.TaskName}__line-{self.line_index}"

class LanguageHub(models.Model):
    """
    Language hub
    """
    name = models.CharField(
        max_length=50, null=True, blank=True,
        help_text="name of language ex. English, Arabic etc",
    )
    short_name = models.CharField(
        max_length=3, null=True, blank=True,
        help_text="short name of language ex. en for English and mar for Marathi",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    

def font_file_path(instance, filename):
    """
    Custom path to upload font file
    """
    return f"fonts/{instance.lang.name}/{filename}"

class FontHub(models.Model):
    """
    Font Hub -- to store all fonts separated by line
    """
    name = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="name of font ex. Times new roman, Helvetica etc..",
    )
    file = models.FileField(upload_to=font_file_path)
    lang = models.ForeignKey(
        LanguageHub, blank=True, on_delete=models.CASCADE,
        help_text="Language in which this font file belongs"
    )
    desc = models.TextField(
        blank=True, null=True,
        help_text="Description of Font"
    )
    desc_html = models.TextField(
        blank=True, null=True,
        help_text="Description of Font in html format"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    

class WordAnnotation(models.Model):
    """
    Word annotations of task
    """
    task = models.ForeignKey(
        Tasks, blank=True, on_delete=models.CASCADE,
        help_text="Task id in which this line annotation belongs"
    )
    word_index = models.IntegerField(
        blank=True, null=True,
        help_text="Word index in image"
    )
    text = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="recognized text",
    )
    lang = models.ForeignKey(
        LanguageHub, blank=True, on_delete=models.CASCADE,
        help_text="Language of word"
    )
    font = models.ForeignKey(FontHub, blank=True, on_delete=models.CASCADE)
    is_bold = models.BooleanField(default=False)
    is_italic = models.BooleanField(default=True)
    box_coordinates = models.TextField(
        null=True, blank=True,
        help_text="Bounding box coordinates. TODO. use ArrayField or JSONfield later"
    )
    left =models.DecimalField(
        decimal_places=2, blank=True,null=True,max_digits=5,
        help_text="left position of annotation"
    )
    top =models.DecimalField(
        decimal_places=2, blank=True,null=True,max_digits=5,
        help_text="top position of annotation"
    )
    heigh =models.DecimalField(
        decimal_places=2, blank=True,null=True,max_digits=5,
        help_text="top position of annotation"
    )
    width =models.DecimalField(
        decimal_places=2, blank=True,null=True,max_digits=5,
        help_text="top position of annotation"
    )
    font_color =models.CharField(
        max_length=255,blank=True,null=True,
        help_text="font color"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task.TaskName}__word-{self.word_index}"


class LineAnnotationExtraInfo(models.Model):
    """
    Save extra info of line annotations such as 
    Grouping of words by line coordinates

    After line-level and word level annotation multiple celery tasks will be performed in that
    1) group_words_by_line_coordinates -- to group the words by line. It will save info here,
      this will be used for meta file generation
    """
    line = models.ForeignKey(
        LineAnnotation, blank=True, on_delete=models.CASCADE,
        help_text="Line annotation for which we are saving extra information"
    )
    grouped_words_annotation_by_line = models.ManyToManyField(
        WordAnnotation, related_name='grouped_words_annotation_by_line',
        blank=True,
        help_text="Word annotation ids that are been grouped together as per line coordinates"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.line.task.TaskName}__line-{self.line.line_index}"


def generated_line_image_path(instance, filename):
    """
    Custom path to upload generated line images part
    """
    return f"cropped_line_imgs/task_{instance.line.task.id}/{filename}"


class LineRendering(models.Model):
    """
    Line rendering preview

    Note:
    In rendering preview - point 7, after resizing line annotations will be updated and again new cropped parts will be stored
    
    TODO:
        1) If image bounding box add option to specify margin, blending options etc..
        2) In rendering preview:
          - We can add shadow and check in realtime
          - change font in realtime
          - change text spacing and other properties
    """
    line = models.ForeignKey(
        LineAnnotation, blank=True, on_delete=models.CASCADE,
        help_text="Line annotation for which we are rendering this line"
    )
    is_multi_lang_parts = models.BooleanField(
        default=False, null=True, blank=True,
        help_text="Is it contains multiple language parts"
    )
    generated_line_image = models.ImageField(upload_to=generated_line_image_path, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.line.task.TaskName}__line-{self.line.line_index}"


class LineRenderingPart(models.Model):
    """
    Storing parts of line image
    - As considering one line may contains multiple language text, so we need to render it separately for that 
    we have created this model
    """
    part_number = models.IntegerField(
        blank=True, null=True,
        help_text="Part index of line"
    )
    line = models.ForeignKey(
        LineAnnotation, blank=True, on_delete=models.CASCADE,
        help_text="Line annotation for which we are rendering this line"
    )
    lang = models.ForeignKey(
        LanguageHub, blank=True, on_delete=models.CASCADE,
        help_text="Language of word"
    )
    font = models.ForeignKey(FontHub, blank=True, on_delete=models.CASCADE)
    text_case = models.CharField(
        max_length=10,
        choices=TEXT_CASE_CHOICES,
        blank=True, null=True,
        help_text="text case 1) lower 2) upper 3) camel"
    )
    stroke_width = models.IntegerField(
        blank=True, null=True,
        default=0,
        help_text="Width of text stroke"
    )
    font_size = models.IntegerField(
        blank=True, null=True,
        default=32,
        help_text="Font size for generated text"
    )
    margin = models.IntegerField(
        blank=True, null=True,
        default=3,
        help_text="Margin to render text"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.line.task.TaskName}__line-{self.line.line_index}_part_{self.part_number}"


def annotation_meta_info_path(instance, filename):
    """
    Custom path to upload images
    """
    return f"annotation_meta_info/task_id_{instance.task.id}/{filename}"

class AnnotationMetaInfo(models.Model):
    """
    Store annotation meta information-- for task
    """
    task = models.ForeignKey(
        Tasks, blank=True, on_delete=models.CASCADE,
        help_text="Task id in which this line annotation belongs"
    )
    is_line_annotation_done = models.BooleanField(
        default=False, null=True, blank=True,
        help_text="Once user perform line level annotations and press save button line annotations will be saved and this will turned to true"
    )
    image_visualized_lines = models.ImageField(
        upload_to=annotation_meta_info_path, null=True, blank=True,
        help_text="image with line level coordinates visualization"
    )
    is_word_annotation_done = models.BooleanField(
        default=False, null=True, blank=True,
        help_text="After word level annotation save this will be turned on"
    )
    image_visualized_words = models.ImageField(
        upload_to=annotation_meta_info_path, null=True, blank=True,
        help_text="image with word level coordinates visualization"
    )
    meta_json_file = models.FileField(
        upload_to="images/", null=True, blank=True,
        help_text="Meta data file to render new id card"
    )
    is_line_data_rendering_done = models.BooleanField(
        default=False, null=True, blank=True,
        help_text="After line and word annotation, background script will generate and render data."
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task.TaskName}"