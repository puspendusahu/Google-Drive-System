var modalEditFolder;
var modalEditFile;
$(function () {
  modalEditFolder = new bootstrap.Modal(document.getElementById('modalEditFolder'), {});
  modalEditFile = new bootstrap.Modal(document.getElementById('modalEditFile'), {});
});

$("#btnAddFolder").click(function () {
  let csr = $("input[name=csrfmiddlewaretoken").val();
  let folderdata = {
    folderName: $("#folderNameId").val(),
    folderDesc: $("#folderDescId").val(),
    parentFolderId: Number($("#hdnAddFolder").attr("data-parentfolderid")),
    csrfmiddlewaretoken: csr
  };

  if (folderdata.folderName == "") {
    alert("Ender folder name.");
  } else if (folderdata.folderDesc == "") {
    alert("Ender Folder Desc.");
  }
  let url = "/addFolderAjax/";
  $.ajax({
    method: "Post",
    url: url,
    data: folderdata,
    success: function (resultArr) {
      if (resultArr.status == 1) {
        location.reload();
      } else {
        confirm("Data not create successfully.");
      }
    },
    error: function (response) {
      alert("System error occured. Kindly contact support.");
    },
  });
});

$(".deleteRootfolder").click(function () {
  $cardFolder = $(this)
    .closest(".card-body")
    .closest(".card")
    .closest(".CardFolder");
  let folderId = Number($(this).data("folderid"));
  let csr = $("input[name=csrfmiddlewaretoken").val();
  let mydata = {
    folderId: folderId,
    csrfmiddlewaretoken: csr
  };
  $.confirm({
    theme: "material",
    title: "Are you sure?",
    content: "Are you sure to delete selected folder?",
    buttons: {
      confirm: function () {
        if (mydata.folderId > 0) {
          $.ajax({
            method: "POST",
            url: "/deletefolder/",
            data: mydata,
            success: function (result) {
              if (result.status > 0) {
                $cardFolder.remove();
                confirm("Data delete successfully.");
              } else confirm("Folder can not deleted.");
            },
            error: function (response) {
              alert("System error occured. Kindly contact support.");
            },
          });
        } else {
          $cardFolder.remove();
        }
      },
      cancel: function () {},
    },
  });
});


$(".editRootfolder").click(function () {
  let folderId = Number($(this).data("folderid"));
  $("#hdnParentFolderId").val('');
  $("#hdnFolderId").val('');
  $("#folderName").val('');
  $("#folderDesc").val('');
  let mydata = {
    folderId: folderId,
  };

  modalEditFolder.show();
  let url = "/editFolderAjax/";
  $.ajax({
    method: "GET",
    url: url,
    data: mydata,
    dataType: 'JSON',
    success: function (resultArr) {
      if(resultArr.status > 0){
        if(resultArr.folderData.parentFolderId != null){
          $("#hdnParentFolderId").val(resultArr.folderData.parentFolderId);
        }
        $("#hdnFolderId").val(folderId);
        $("#folderName").val(resultArr.folderData.folderName);
        $("#folderDesc").val(resultArr.folderData.folderDesc);
      }else{
        confirm("Data not available");
      }
    },
    error: function (response) {
      alert("System error occured. Kindly contact support.");
    },
  });
});


$("#rootBtnSubmit").click(function () {
  let csr = $("input[name=csrfmiddlewaretoken").val();
  let folderdata = {
    parentFolderId: $("#hdnParentFolderId").val(),
    folderId: Number($("#hdnFolderId").val()),
    folderName: $("#folderName").val(),
    folderDesc: $("#folderDesc").val(),
    csrfmiddlewaretoken: csr,
  };

  if (folderdata.folderName == "") {
    alert("Ender folder name.");
  } else if (folderdata.folderDesc == "") {
    alert("Ender Folder Desc.");
  }
  let url = "/editFolderAjaxPost/";
  $.ajax({
    method: "Post",
    url: url,
    data: folderdata,
    success: function (resultArr) {
      if (resultArr.status == 1) {
        location.reload();
      } else {
        confirm("Data not create successfully.");
      }
    },
    error: function (response) {
      alert("System error occured. Kindly contact support.");
    },
  });
});


$(".deleteFile").click(function () {
  $cardFile = $(this)
    .closest(".card-body")
    .closest(".card")
    .closest(".cardFile");
  
  let csr = $("input[name=csrfmiddlewaretoken").val();
  let fileId = Number($(this).data("fileid"));
  let mydata = {
    fileId: fileId,
    csrfmiddlewaretoken: csr
  };
  $.confirm({
    theme: "material",
    title: "Are you sure?",
    content: "Are you sure to delete selected file?",
    buttons: {
      confirm: function () {
        if (mydata.fileId > 0) {
          $.ajax({
            method: "POST",
            url: "/deleteFile/",
            data: mydata,
            success: function (result) {
              if (result.status > 0) {
                $cardFile.remove();
                confirm("File delete successfully.");
              } else confirm("File can not deleted.");
            },
            error: function (response) {
              alert("System error occured. Kindly contact support.");
            },
          });
        } else {
          $cardFile.remove();
        }
      },
      cancel: function () {},
    },
  });
});


$(".editFile").click(function () {
  let fileId = Number($(this).data("fileid"));
  $("#hdnFileId").val('');
  $("#fileName").val('');
  let mydata = {
    fileId: fileId,
  };

  modalEditFile.show();
  let url = "/editFileAjax/";
  $.ajax({
    method: "GET",
    url: url,
    data: mydata,
    dataType: 'JSON',
    success: function (resultArr) {
      debugger;
      if(resultArr.status > 0){
        $("#hdnFileId").val(fileId);
        $("#fileName").val(resultArr.fileData.fileTitle);
      }else{
        confirm("Data not available");
      }
    },
    error: function (response) {
      alert("System error occured. Kindly contact support.");
    },
  });
});


$("#fileBtnSubmit").click(function () {
  let csr = $("input[name=csrfmiddlewaretoken").val();
  let filedata = {
    fileId: Number($("#hdnFileId").val()),
    folderId: Number($("#hdnMainFolderId").val()),
    fileName: $("#fileName").val(),
    csrfmiddlewaretoken: csr
  };

  if (filedata.fileName == "") {
    alert("Ender file name.");
  }

  let url = "/editFileAjaxPost/";
  $.ajax({
    method: "Post",
    url: url,
    data: filedata,
    success: function (resultArr) {
      if (resultArr.status == 1) {
        location.reload();
      } else {
        confirm("Data not create successfully.");
      }
    },
    error: function (response) {
      alert("System error occured. Kindly contact support.");
    },
  });
});