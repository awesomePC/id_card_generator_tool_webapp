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
    CreatedOnDate=models.DateTimeField(auto_now=True,null=True, blank=True)
    CreateByUserId=models.ForeignKey(Users,related_name='createdTasks', null=True, blank=True, on_delete=models.DO_NOTHING)
    UpdatedDate=models.DateTimeField(auto_now=True,null=True, blank=True)
    UpdatedByUserId=models.ForeignKey(Users,related_name='updatedTasks', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.TaskName