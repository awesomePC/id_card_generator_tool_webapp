from django.db import models
from auth.models import Users
from projects.models import Projects

# Create your models here.
class Tasks(models.Model):
    TaskName=models.CharField(max_length=255, null=True, blank=True)
    ProjectId=models.ForeignKey(Projects,related_name='tasks', blank=True,on_delete=models.DO_NOTHING)
    MainImageFile =models.TextField(null=True, blank=True)
    TextRemovedImageFile=models.TextField(null=True, blank=True)
    WordAnnotationList=models.TextField(null=True, blank=True)
    CreatedOnDate=models.DateTimeField(auto_now=True,null=True, blank=True)
    CreateByUserId=models.ForeignKey(Users,related_name='createdTasks', blank=True,on_delete=models.DO_NOTHING)
    UpdatedDate=models.DateTimeField(auto_now=True,null=True, blank=True)
    UpdatedByUserId=models.ForeignKey(Users,related_name='updatedTasks', blank=True,on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.TaskName