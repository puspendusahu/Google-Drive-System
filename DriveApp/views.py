from django.shortcuts import redirect, render, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Folder, File
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict


def index(request):
    if request.user.is_authenticated:
        folder = Folder.objects.filter(
            folderUser=request.user, parentFolderId__isnull=True
        )
        context = {"folder": folder}
        return render(request, "DriveApp/index.html", context)
    else:
        return redirect("signup")


# Go Folder with files in it
def folder(request, folderid):
    if request.user.is_authenticated:
        folder_user = Folder.objects.get(id=folderid)
        childFolder = Folder.objects.filter(parentFolderId=folderid)
        files = File.objects.filter(folder=folder_user)
        context = {"folderid": folderid, "files": files, "childFolder": childFolder}
        if request.method == "POST":
            file_user = request.FILES.get("file")
            file_title = request.POST.get("filetitle")
            fileadd = File.objects.create(
                fileTitle=file_title, file=file_user, folder=folder_user
            )
            return HttpResponseRedirect("/folder/%i/" % folderid)
        else:
            return render(request, "DriveApp/folder.html", context)
    else:
        return redirect("signup")


# Add Folder View
def addfolder(request):
    if request.method == "POST":
        folder_name = request.POST["foldername"]
        folder_desc = request.POST["desc"]
        folder = Folder.objects.create(
            folderName=folder_name, folderDesc=folder_desc, folderUser=request.user
        )
        if folder:
            return redirect("index")
        else:
            messages.error(request, "Folder Not Created")
            return redirect("index")


# deletefolder Folder
def deletefolder(request):
    if request.method == "POST":
        folderId = request.POST.get("folderId")
        childFolderData = Folder.objects.filter(
            folderUser=request.user, parentFolderId=folderId
        )
        for i in childFolderData:
            i.delete()
        mainFolderData = Folder.objects.filter(folderUser=request.user, id=folderId)
        mainFolderData.delete()
        return JsonResponse({"status": 1})
    else:
        return JsonResponse({"status": 0})


# Add Folder Ajax View
def addFolderAjax(request):
    if request.method == "POST":
        folder_name = request.POST["folderName"]
        folder_desc = request.POST["folderDesc"]
        parent_Folder_Id = request.POST["parentFolderId"]
        folder = Folder.objects.create(
            folderName=folder_name,
            folderDesc=folder_desc,
            folderUser=request.user,
            parentFolderId=parent_Folder_Id,
        )
        if folder:
            return JsonResponse({"status": 1})
        else:
            return JsonResponse({"status": 0})
    else:
        return JsonResponse({"status": 0})


def editFolderAjax(request):
    if request.method == "GET":
        folder_id = request.GET["folderId"]
        folderObj = Folder.objects.get(id=folder_id)
        dicFolderData = model_to_dict(folderObj)
        return JsonResponse({"status": 1, "folderData": dicFolderData})

def editFolderAjaxPost(request):
    if request.method == "POST":
        folder_Id = request.POST["folderId"]
        parent_Folder_Id = request.POST["parentFolderId"]
        folder_name = request.POST["folderName"]
        folder_desc = request.POST["folderDesc"]
        user = request.user
        if parent_Folder_Id == "":
            folderObj = Folder(
                id=folder_Id,
                folderName=folder_name,
                folderDesc=folder_desc,
                folderUser=user,
            )
            folderObj.save()
        else:
            folderObj = Folder(
                id=folder_Id,
                folderName=folder_name,
                folderDesc=folder_desc,
                folderUser=user,
                parentFolderId=parent_Folder_Id,
            )
            folderObj.save()
        return JsonResponse({"status": 1, "folder_Id": folder_Id})
    else:
        return JsonResponse({"status": 0})


# File Section

def editFileAjaxPost(request):
    if request.method == "POST":
        file_Id = request.POST["fileId"]
        file_name = request.POST["fileName"]
        fileIns = File.objects.get(id=file_Id)
        fileIns.fileTitle = file_name
        fileIns.save()
        return JsonResponse({"status": 1, "file_Id": file_Id})
    else:
        return JsonResponse({"status": 0})


def editFileAjax(request):
    if request.method == "GET":
        file_id = request.GET["fileId"]
        fileObj = File.objects.get(id=file_id)
        file_data = {"id": fileObj.id, "fileTitle": fileObj.fileTitle}
        return JsonResponse({"status": 1, "fileData": file_data})


def deleteFile(request):
    if request.method == "POST":
        fileId = request.POST.get("fileId")
        fileData = File.objects.get(id=fileId)
        fileData.delete()
        return JsonResponse({"status": 1})
    else:
        return JsonResponse({"status": 0})



# View For SignUp the user
def SignUp(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method == "POST":
            username = request.POST["username"]
            email = request.POST["email"]
            password = request.POST["password"]
            cpassword = request.POST["cpassword"]
            firstname = request.POST["fname"]
            lname = request.POST["lname"]
            if username and password and email and cpassword and firstname and lname:
                if password == cpassword:
                    user = User.objects.create_user(username, email, password)
                    user.first_name = firstname
                    user.last_name = lname
                    user.save()
                    if user:
                        messages.success(request, "User Account Created")
                        return redirect("login")
                    else:
                        messages.error(request, "User Account Not Created")
                else:
                    messages.error(request, "Password Not Matched")
                    redirect("signup")
        return render(request, "DriveApp/signup.html")


# View For Log in the user
def Login(request):
    if request.user.is_authenticated:
        return redirect("login")
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            if username and password:
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect("index")
        return render(request, "DriveApp/login.html")


# User logout function
def Logout(request):
    logout(request)
    return redirect("index")
