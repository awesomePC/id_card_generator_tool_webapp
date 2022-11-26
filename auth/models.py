from django.db import models

# Create your models here.
class UserRoles(models.Model):
    Name=models.TextField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.Name

class Users(models.Model):
    FirstName=models.TextField(max_length=255, null=True, blank=True)
    LastName=models.TextField(max_length=255, null=True, blank=True)
    Email=models.TextField(null=True, blank=True)
    IsActive=models.BooleanField(default=True)
    Password=models.TextField(null=True, blank=True)
    CreatedDate=models.DateTimeField(auto_now=True)
    UpdatedDate=models.DateTimeField(auto_now=True)

    Role=models.ForeignKey(UserRoles,related_name='Users', blank=True,on_delete=models.DO_NOTHING)
    
    def __str__(self):
        return self.FirstName