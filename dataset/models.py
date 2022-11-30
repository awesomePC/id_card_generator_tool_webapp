from django.db import models
from auth.models import Users
from tasks.models import Tasks
from dataset.choices import (
    EXPORTED_DATASET_TYPE_CHOICES,
    ANNOTATION_TYPE_CHOICES,
    ANNOTATION_FORMAT_CHOICES,
    EXPORTED_FILE_FORMAT_CHOICES
)

# Create your models here.

class Dataset(models.Model):
    """
    generated dataset

    After creating the metadata and verifying the preview of card generation, you can generate dataset of completed task
    
    TODO: Get status information
    """
    name = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="name of dataset ex. pan_card_format_1_10k",
    )
    desc = models.TextField(
        blank=True, null=True,
        help_text="Description of dataset"
    )
    desc_html = models.TextField(
        blank=True, null=True,
        help_text="Description of dataset in html format"
    )
    task = models.ForeignKey(
        Tasks, blank=True, on_delete=models.DO_NOTHING,
        help_text="Task id in which this dataset belongs"
    )
    count = models.IntegerField(
        blank=True, null=True,
        default=5,
        help_text="how many images to generate"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name 
    

def dataset_resource_path(instance, filename):
    """
    Custom path to upload dataset images and annotation files
    """
    return f"dataset/task_id_{instance.dataset.task.id}/dataset_id_{instance.dataset.id}/{filename}"


class DatasetResource(models.Model):
    """
    generated images and annotations of dataset
    """
    dataset = models.ForeignKey(
        Tasks, blank=True, on_delete=models.DO_NOTHING,
        help_text="Dataset in which this image belongs"
    )
    image = models.ImageField(upload_to=dataset_resource_path, null=True, blank=True)
    annotation_file = models.FileField(upload_to=dataset_resource_path)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.dataset.name 


#########################################################################################################

class ExportedDataset(models.Model):
    """
    In exported dataset we can combine multiple dataset and export either recognition, detection or both
    with splitting set, train - 70% , val - 15% and test 15 %

    in various annotation format.
    """
    name = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="name of dataset ex. pan_card_format_1_10k",
    )
    type = models.CharField(
        max_length=15,
        choices=EXPORTED_DATASET_TYPE_CHOICES,
        help_text="type of dataset 1) detection 2) recognition"
    )
    annotation_type = models.CharField(
        max_length=15,
        choices=ANNOTATION_TYPE_CHOICES,
        help_text="type of annotation either line_level or word_level"
    )
    annotation_format = models.CharField(
        max_length=15,
        choices=ANNOTATION_FORMAT_CHOICES,
        help_text="format of annotation to export such as ppocrlabel, icdar2015, easyocr, mmocr etc.."
    )

    desc = models.TextField(
        blank=True, null=True,
        help_text="Description of dataset"
    )
    desc_html = models.TextField(
        blank=True, null=True,
        help_text="Description of dataset in html format"
    )

    train_set_percentage = models.PositiveIntegerField(
        blank=True, null=True,
        default=70,
        help_text="Training set percentage"
    )
    val_set_percentage = models.PositiveIntegerField(
        blank=True, null=True,
        default=15,
        help_text="Validation set percentage"
    )
    test_set_percentage = models.PositiveIntegerField(
        blank=True, null=True,
        default=15,
        help_text="Testing set percentage"
    )

    out_directory_path = models.TextField(
        blank=True, null=True,
        help_text="Root Folder path to store images and other files -- can be auto generated"
    )
    exported_file_format = models.CharField(
        max_length=15,
        blank=True, null=True,
        default=".zip",
        choices=EXPORTED_FILE_FORMAT_CHOICES,
        help_text="format of compressed file such as .zip, .tar etc"
    )
    exported_file = models.FileField(upload_to="exported_dataset/")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey(
        Users, blank=True, on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return self.name 