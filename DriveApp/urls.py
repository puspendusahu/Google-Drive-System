from django.urls import path
from .import views
urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.Login, name="login"),
    path("signup/",views.SignUp,name="signup"),
    path("logout/", views.Logout, name="logout"),


    path("folder/<int:folderid>/",views.folder, name="folder"),
    path("addFolder/", views.addfolder, name="addfolder"),
    path("addFolderAjax/", views.addFolderAjax, name="addFolderAjax"),       
    path("deletefolder/",views.deletefolder, name="deletefolder"),
    path("editFolderAjax/",views.editFolderAjax, name="editFolderAjax"),
    path("editFolderAjaxPost/",views.editFolderAjaxPost, name="editFolderAjaxPost"),

    path("deleteFile/",views.deleteFile, name="deleteFile"),
    path("editFileAjax/",views.editFileAjax, name="editFileAjax"),
    path("editFileAjaxPost/",views.editFileAjaxPost, name="editFileAjaxPost"),
]
