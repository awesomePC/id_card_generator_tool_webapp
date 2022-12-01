from django.db import models
from auth.models import Users
from annotation.choices import CONTENT_TYPE_CHOICES
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
        Users, related_name='createdByUser', blank=True, null=True, on_delete=models.DO_NOTHING
    )
    updated_by_user = models.ForeignKey(
        Users, related_name='updatedByUser', blank=True, null=True, on_delete=models.DO_NOTHING
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
        Tasks, blank=True, on_delete=models.DO_NOTHING,
        help_text="Task id in which this line annotation belongs"
    )
    dict = models.ForeignKey(DictionaryHub, blank=True, on_delete=models.DO_NOTHING)
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
        LanguageHub, blank=True, on_delete=models.DO_NOTHING,
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
    word_index = models.IntegerField(
        blank=True, null=True,
        help_text="Word index in image"
    )
    text = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="recognized text",
    )
    lang = models.ForeignKey(
        LanguageHub, blank=True, on_delete=models.DO_NOTHING,
        help_text="Language of word"
    )
    font = models.ForeignKey(FontHub, blank=True, on_delete=models.DO_NOTHING)
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
    task = models.ForeignKey(
        Tasks, blank=True, on_delete=models.DO_NOTHING,
        help_text="Task id in which this line annotation belongs"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.task.TaskName}__word-{self.word_index}"
