from django.db import models
from auth.models import Users
from tasks.models import Tasks
from dataset.models import Dataset
from export.choices import (
    EXPORTED_DATASET_TYPE_CHOICES,
    ANNOTATION_TYPE_CHOICES,
    ANNOTATION_FORMAT_CHOICES,
    EXPORTED_FILE_FORMAT_CHOICES
)

# Create your models here.
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
    source_datasets = models.ManyToManyField(
        Dataset, related_name='source_datasets',
        blank=True,
        help_text="source dataset that has been used to export this data. It amy be one or more"
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