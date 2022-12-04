from django.db import models
from auth.models import Users
from export.models import ExportedDataset
from training.choices import STATUS_CHOICES

# Create your models here.

class TrainingHub(models.Model):
    """
    Store training related information

    Args:
        models (_type_): _description_
    """
    name = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="name of training",
    )
    desc = models.TextField(
        blank=True, null=True,
        help_text="Description of Training"
    )
    dataset = models.ForeignKey(
        ExportedDataset, blank=True, on_delete=models.DO_NOTHING,
        help_text="dataset on which we are performing training"
    )
    remote_ip = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Remote GPU server ip to connect for distributed training",
    )
    gpu_ids = models.CharField(
        max_length=255, null=True, blank=True,
        help_text="Comma separated list of GPU id",
    )
    input_checkpoint_file = models.FileField(
        upload_to="checkpoints/input/",
        null=True, blank=True,
        help_text="model checkpoint for resuming training if any"
    )
    output_checkpoint_file = models.FileField(
        upload_to="checkpoints/output/",
        null=True, blank=True,
        help_text="output directory to store model checkpoint"
    )
    status = models.CharField(
        max_length=15,
        blank=True, null=True,
        choices=STATUS_CHOICES,
        help_text="Status of process"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by_user = models.ForeignKey(
        Users, blank=True, on_delete=models.DO_NOTHING
    )
