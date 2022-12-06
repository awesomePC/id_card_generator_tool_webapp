  
//Preview
var previewCanvas = new fabric.Canvas('previewCanvas');
var enableZoom = false;
var imageHeight = 0;
var imageWidth = 0;
// var myModal = new bootstrap.Modal(document.getElementById('CanvasModal'), {
//     keyboard: false
// })

$(document).ready(function () {
    
    // canvas.setHeight(410);
    // canvas.setWidth(600);
    fabric.Object.prototype.setControlsVisibility({
        mtr: false,
    });
    // $.ajax({
    //     url:`{{ url 'lineannodata'}}`
    // })
})

// show image after loading automatically if task selected
if (typeof preview_task_id !== 'undefined') {
    $("#frmPreviewTask").val(preview_task_id)
    if(preview_task_id != 0) {
        fetch('/task_detail?id=' + preview_task_id).then(r => r.json()).then(r => {
            imagePath = '/media/' + r.MainImageFile;
            addImageInPreviewCanvas(imagePath);
            if(previewAnnotations.length > 0){    
              var  taskPreviewAnnotations=JSON.parse(localStorage.getItem("taskAnnotations"))
              var taskId = $('#frmPreviewTask').val();  
              taskPreviewAnnotations =previewAnnotations // taskPreviewAnnotations.filter(i=>i.task==taskId);  
              if(taskPreviewAnnotations.length > 0){
              setTimeout(function(){
            for (var i = 0; i < taskPreviewAnnotations.length; i++) {
                AddLineRenderingPreviewCanvas(taskPreviewAnnotations[i])
            }   
        },500)}else{
            alert("For selected task no any preview saved yet. Please go to Annotate-> World level and create preview.")
        }
            }
       
        });
    }
} 

// page reload accoring to task_id
$("#frmPreviewTask").change(function (e) {
    let id = $("#frmPreviewTask option:selected").val();
    if(id > 0){
    window.location.replace(`/annotate/preview?id=${id}`);
    }else{
        window.location.replace(`/annotate/preview`);
    }
})


function addImageInPreviewCanvas(imagepath) {
    fabric.Image.fromURL(imagepath, function (img) {
        previewCanvas.clear();  
        imageHeight = img.height;
        imageWidth = img.width;
        img.set({
            originX: 'left',
            originY: 'top',
            objectCaching: false,
            fill: 'transparent',
            selectable: false,
            type: "image",
            opacity:0.5
        });
        previewCanvas.setHeight(img.height);
        previewCanvas.setWidth(img.width); 
        previewCanvas.add(img).renderAll();
    });
}


function AddLineRenderingPreviewCanvas(renderObj) {
    
    fabric.Image.fromURL('/media/images/dummy.jpg', function (img) {
        
        img.set({
            originX: 'left',
            originY: 'top', 
            left: renderObj.left,
        top: renderObj.top, 
            height: renderObj.height, 
        width: renderObj.width,
            fill: 'transparent',
            selectable: true,
            type: "image",
            
        }); 
        previewCanvas.add(img).renderAll();
    }); 
   
 }

 
function ZoomIn() {
    $(".btnFunction").removeClass("selected")
    $(".btnZoomIn").addClass("selected")
    enableZoom = true;
    // debugger
    previewCanvas.zoomToPoint(new fabric.Point(previewCanvas.width / 2, previewCanvas.height / 2), previewCanvas.getZoom() + 0.1);
    previewCanvas.setWidth(imageWidth * previewCanvas.getZoom() + 0.1);
    previewCanvas.setHeight(imageHeight * previewCanvas.getZoom() + 0.1);
    previewCanvas.setViewportTransform([previewCanvas.getZoom(), 0, 0, previewCanvas.getZoom(), 0, 0]);
}

function ZoomOut() {
    $(".btnFunction").removeClass("selected")
    $(".btnZoomOut").addClass("selected")
    enableZoom = true;
    previewCanvas.zoomToPoint(new fabric.Point(previewCanvas.width / 2, previewCanvas.height / 2), previewCanvas.getZoom() - 0.1);
    previewCanvas.setWidth(imageWidth * previewCanvas.getZoom() - 0.1);
    previewCanvas.setHeight(imageHeight * previewCanvas.getZoom() - 0.1);
    previewCanvas.setViewportTransform([previewCanvas.getZoom(), 0, 0, previewCanvas.getZoom(), 0, 0]);
}
function DefaultZoom() {
    $(".btnFunction").removeClass("selected")
    $(".btnResetZoom").addClass("selected")
    enableZoom = false;
    previewCanvas.setWidth(imageWidth);
    previewCanvas.setHeight(imageHeight);
    previewCanvas.setViewportTransform([1, 0, 0, 1, 0, 0]);
}

function DisableZoom() {
    $(".btnFunction").removeClass("selected")
    $(".btnDisableZoom").addClass("selected")
    enableZoom = false;
}

