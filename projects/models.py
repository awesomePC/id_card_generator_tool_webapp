from django.db import models
from auth.models import Users

# Create your models here.
class Projects(models.Model):
    Name = models.CharField(max_length=255, null=True, blank=True)
    CreatedOnDate=models.DateTimeField(auto_now=True)
    CreateByUserId=models.ForeignKey(
        Users,related_name='createdProjects', on_delete=models.DO_NOTHING,
        null=True, blank=True
    )
    UpdatedDate=models.DateTimeField(auto_now=True, null=True, blank=True)
    UpdatedByUserId=models.ForeignKey(
        Users,related_name='updatedProjects', on_delete=models.DO_NOTHING,
        null=True, blank=True
    )

    def __str__(self):
        return self.Name