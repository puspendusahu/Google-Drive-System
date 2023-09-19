from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Folder(models.Model):
    folderName = models.CharField(max_length=50)
    folderDesc = models.CharField(max_length=255)
    folderUser = models.ForeignKey(User,on_delete=models.CASCADE)
    parentFolderId = models.IntegerField(null=True)

class File(models.Model):
    fileTitle = models.CharField(max_length=50)
    folder = models.ForeignKey(Folder,on_delete=models.CASCADE)
    file = models.FileField(upload_to="Files")