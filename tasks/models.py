from django.db import models
from auth.models import Users
from projects.models import Projects

# Create your models here.
class Tasks(models.Model):
    """
    Managing tasks of project -- single project will contains multiple tasks
    """
    TaskName=models.CharField(max_length=255, null=True, blank=True)
    ProjectId=models.ForeignKey(Projects,related_name='tasks', blank=True,on_delete=models.DO_NOTHING)
    MainImageFile =models.ImageField(upload_to='images/',null=True, blank=True)
    TextRemovedImageFile=models.ImageField(upload_to='images/',null=True, blank=True)
    is_line_annotation_done = models.BooleanField(
        default=False, null=True, blank=True,
        help_text="Once user perform line level annotations and press save button line annotations will be saved and this will turned to true"
    )
    is_word_annotation_done = models.BooleanField(
        default=False, null=True, blank=True,
        help_text="After word level annotation save this will be turned on"
    )
    meta_json_file = models.FileField(
        upload_to="images/", null=True, blank=True,
        help_text="Meta data file to render new id card"
    )
    CreatedOnDate=models.DateTimeField(auto_now=True,null=True, blank=True)
    CreateByUserId=models.ForeignKey(Users,related_name='createdTasks', null=True, blank=True, on_delete=models.DO_NOTHING)
    UpdatedDate=models.DateTimeField(auto_now=True,null=True, blank=True)
    UpdatedByUserId=models.ForeignKey(Users,related_name='updatedTasks', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.TaskName