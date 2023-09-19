from django.contrib import admin
from .models import File, Folder
# Register your models here.

@admin.register(Folder)
class Adminfolder(admin.ModelAdmin):
   list_display = ('folderName','folderUser')
   
@admin.register(File)
class Adminfolder(admin.ModelAdmin):
   list_display = ('id','file','fileTitle')