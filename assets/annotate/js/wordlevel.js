var canvas = new fabric.Canvas('mainCanvas');
var enableZoom = false;
var imageHeight = 0;
var imageWidth = 0;
var polygonMode = false;
var startingPolygonPoint;
var pointArray = new Array();
var lineArray = new Array();
var activeLine;
var activeShape = false;
var min = 99;
var max = 999999;
var isRectangleStarted = false;
var x = 0;
var y = 0;
var mY = 0;
var mX = 0;
var mouseDown = false;
let pos = { top: 0, left: 0, x: 0, y: 0 };
var movableImage = false;
var annotationFieldIDs = []

//Preview
var previewCanvas = new fabric.Canvas('previewCanvas');

// var myModal = new bootstrap.Modal(document.getElementById('CanvasModal'), {
//     keyboard: false
// })

$(document).ready(function () {
    
    // canvas.setHeight(410);
    // canvas.setWidth(600);
    fabric.Object.prototype.setControlsVisibility({
        mtr: false,
    });
})

// show image after loading automatically if task selected
if (typeof taskID !== 'undefined') {
    if(taskID != 0) {
        fetch('/task_detail?id=' + taskID).then(r => r.json()).then(r => {
            imagePath = '/media/' + r.MainImageFile;
            addImageInCanvas(imagePath);
        });
    }
}

window.onload = function () {
    setTimeout(() => {
        initialShow();
    }, 200)
}

// page reload accoring to task_id
$("#frmTask").change(function (e) {
    let id = $("#frmTask option:selected").val();
    window.location.replace(`/annotate/wordlevel/${id}`);
})


function initialShow() {
    //show right side forms according to annotations
    if (typeof isAnnoExist !== 'undefined') {
        if (isAnnoExist) {
            let template = ``;
            let temp;
            for (let i = 0; i < annotations.length; i++) {
                // annotationFieldIDs.push(`canvas_${i}`);
                template += 
                    `<div class="card mb-2 annotation_card selected" id='canvas_${i}'>
                        <div class="card-body">
                            <input id="text" type="text" 
                                value=${annotations[i].text} 
                                class="form-control mb-2 txtRecognize" 
                                title="text label"
                            />
                            <select onchange="selectFonts(this.value, 'canvas_${i}')" id="lang" class="form-select mb-2 ddlLanguage" aria-label="text" title="Language Selection">`
                            for(let k = 0; k<langs_data.length; k++){
                                if(langs_data[k].id == annotations[i].lang_id) {
                                    temp = k;
                                    template +=`<option value="${langs_data[k].id}" selected>${langs_data[k].name}</option>`;
                                } else {
                                    template +=`<option value="${langs_data[k].id}">${langs_data[k].name}</option>`;
                                }
                            }    
                            template += ` </select>
                            <select id="font" class="form-select mb-2 ddlFont" aria-label="text" title="Font Selection">`;
                            for(let j = 0; j<langs_data[temp].fonts.length; j++) {
                                if(langs_data[temp].fonts[j] == annotations[i].font_id) {
                                    template +=`<option value="${langs_data[temp].fonts[j].id}" selected>${langs_data[temp].fonts[j].name}</option>`;
                                } else {
                                    template +=`<option value="${langs_data[temp].fonts[j].id}">${langs_data[temp].fonts[j].name}</option>`;
                                }
                            }
                            template +=`</select>
                            <div class="form-check mb-2">
                                <input class="form-check-input chkIsBold" type="checkbox" id="check1" name="option1" value="something"`
                                if (annotations[i].is_bold == 1)
                                    template += `checked`;
                                template +=`>
                                <label class="form-check-label">Is Bold</label>
                            </div>
                            <div class="form-check mb-2">
                                <input class="form-check-input chkIsItalic" type="checkbox" id="check2" name="option2" value="something"`
                                if (annotations[i].is_italic == 1)
                                    template += `checked`;
                                template +=`>
                                <label class="form-check-label">Is Italic</label>
                            </div>
                            <div class="form-group mb-2">
                                <input class="form-control form-control-solid  h-40px p-1 w-40px txtColor" title="select Color" type="color" value="something" >
                            </div>
                        </div>
                    </div>`;
                
                
                let box_coordinates = JSON.parse(annotations[i].box_coordinates)
                console.log(box_coordinates)
                //draw rect according to coordinate data
                let guid = 'canvas_' + i
                let square = new fabric.Rect({
                    width: box_coordinates[1][0]-box_coordinates[0][0],
                    height: box_coordinates[2][1]-box_coordinates[1][1],
                    left: box_coordinates[0][0],
                    top: box_coordinates[0][1],
                    new: 0,
                    fill: 'transparent',
                    stroke: $('.txtColor').val(),
                    strokeWidth: 1,
                    canvasId: guid
                }).setCoords();
                canvas.add(square);
                canvas.renderAll();
                // canvas.setActiveObject(square);
                console.log(square.aCoords)
             }
             $(".dvAnnotationFields").html(template);
        }
    }
    
}

$(".btnDrawRectangle").click(function () {
    isRectangleStarted = true;
    canvas.discardActiveObject()
    $(".btnFunction").removeClass("selected")
    $(this).addClass("selected")
})

$(".dvParentCanvas").mousemove(function (e) {
    if (movableImage) {
        const dx = e.clientX - pos.x;
        const dy = e.clientY - pos.y;

        // Scroll the element
        $(".dvParentCanvas")[0].scrollTop = pos.top - dy;
        $(".dvParentCanvas")[0].scrollLeft = pos.left - dx;
    }
});

$(".dvParentCanvas").mousedown(function (e) {
    if (!canvas.getActiveObject()) {
        pos = {
            // The current scroll
            left: $(".dvParentCanvas")[0].scrollLeft,
            top: $(".dvParentCanvas")[0].scrollTop,
            // Get the current mouse position
            x: e.clientX,
            y: e.clientY,
        };
        movableImage = true;
    }
});

$(".dvParentCanvas").mouseup(function (e) {
    movableImage = false;
})

/*
Function to generate annotation template
*/
function get_annotation_template(text, canvas_guid) {
    var template = `
        <div class="card mb-2 annotation_card selected" id=${canvas_guid}>
            <div class="card-body">
                <input id="text" type="text" 
                    value=${text} 
                    class="form-control mb-2 txtRecognize" 
                    title="text label"
                />
                <select onchange="selectFonts(this.value, '${canvas_guid}')" id="lang" class="form-select mb-2 ddlLanguage" aria-label="text" title="Language Selection">`
                for(let i = 0; i<langs_data.length; i++){
                    if(i == 0) {
                        template +=`<option value="${langs_data[i].id}" selected>${langs_data[i].name}</option>`;
                    } else {
                        template +=`<option value="${langs_data[i].id}">${langs_data[i].name}</option>`;
                    }
                }    
                template += ` </select>
                <select id="font" class="form-select mb-2 ddlFont" aria-label="text" title="Font Selection">`;
                for(let j = 0; j<langs_data[0].fonts.length; j++) {
                    if(j == 0) {
                        template +=`<option value="${langs_data[0].fonts[j].id}" selected>${langs_data[0].fonts[j].name}</option>`;
                    } else {
                        template +=`<option value="${langs_data[0].fonts[j].id}">${langs_data[0].fonts[j].name}</option>`;
                    }
                }
                template +=`</select>
                <div class="form-check mb-2">
                <input class="form-check-input chkIsBold" type="checkbox" id="check1" name="option1" value="something">
                <label class="form-check-label">Is Bold</label>
            </div>
            <div class="form-check mb-2">
                <input class="form-check-input chkIsItalic" type="checkbox" id="check2" name="option2" value="something" checked>
                <label class="form-check-label">Is Italic</label>
            </div>
            <div class="form-group mb-2">
                <input class="form-control form-control-solid  h-40px p-1 w-40px txtColor" title="select Color" type="color" value="something" >
            </div>
            </div>
        </div>`
    return template;
}

function selectFonts(value, containerID) {
    
    let parentDiv = document.getElementById(containerID);

    for(let i = 0; i<langs_data.length; i++) {
        if(value == langs_data[i].id) {
            let temp = ``
            for(let j = 0; j<langs_data[i].fonts.length; j++) {
                if(j == 0) {
                    temp +=`<option value="${langs_data[i].fonts[j].id}" selected>${langs_data[i].fonts[j].name}</option>`;
                } else {
                    temp +=`<option value="${langs_data[i].fonts[j].id}">${langs_data[i].fonts[j].name}</option>`;
                }
                parentDiv.querySelector(".ddlFont").innerHTML = "";
                parentDiv.querySelector(".ddlFont").innerHTML = temp;
                
            }
            break;
        }
    }
   
}
$("#img").change(function (e) {
    canvas.clear();
    $(".dvAnnotationFields").html('')
    $("#CanvasModalLabel").text(e.target.files[0].name)
    var reader = new FileReader();
    reader.onload = function (event) {
        var imgObj = new Image();
        imgObj.src = event.target.result;
        imgObj.onload = function () {

            canvas.setHeight(this.height);
            canvas.setWidth(this.width);
            var maxImageHeight = ($(window).height() / 100) * 60;
            imageHeight = this.height;
            imageWidth = this.width;
            $(".dvParentCanvas").css({
                "max-height": (this.height > maxImageHeight ? maxImageHeight : this.height) + "px",
                "max-width": this.width + "px"
            })
            var canvasImg = new fabric.Image(imgObj, {
                originX: 'left',
                originY: 'top',
                objectCaching: false,
                fill: 'transparent',
                selectable: false,
                type: "image",
                hoverCursor: "default"
            })
            canvas.add(canvasImg);
            // myModal.show()

        }
    }
    reader.readAsDataURL(e.target.files[0]);
})

$(".btnAutoRecognise").click(function () {
    var form = new FormData($('.autoRecogniseForm')[0]);

    var settings = {
        "url": "https://304c-216-48-181-201.in.ngrok.io/ocr_api",
        "method": "POST",
        "timeout": 0,
        "processData": false,
        "mimeType": "multipart/form-data",
        "contentType": false,
        "data": form,
        "crossDomain": true,
    };

    $.ajax(settings).done(function (result) {
        var response = JSON.parse(result)
        //box coord 1. left,top 2. right top 3. right bottom 4. left bottom 
        var recognitionFields = ''
        for (var i = 0; i < response.final_processed_result.length; i++) {
            var left = response.final_processed_result[i].box[0][0];
            var top = response.final_processed_result[i].box[0][1];
            var right = response.final_processed_result[i].box[1][0];
            var bottom = response.final_processed_result[i].box[2][1];
            var width = right - left;
            var height = bottom - top;
            var guid = 'canvas_' + CreateGuid()
            var obj = new fabric.Rect({
                left: left,
                top: top,
                fill: 'transparent',
                width: width,
                height: height,
                stroke: $('.txtColor').val(),
                strokeWidth: 1,
                selection: true,
                selectable: true,
                hasControls: true,
                canvasId: guid,
                originX: 'left',
                originY: 'top',
                setControlVisible: {
                    "mtr": false
                }
            }).setCoords();
            canvas.add(obj);
            obj.on('selected', function (e) {
                CanvasObjectSelected(e);
            });

            recognitionFields += get_annotation_template(
                response.final_processed_result[i].text,
                guid
            )
        }
        $(".dvAnnotationFields").html(recognitionFields)
    });
})

$(document).on("click", ".txtRecognize", function () {
    var parent_card = $(this).closest(".annotation_card");
    var guid = $(parent_card).attr("id")
    $(".annotation_card").removeClass("selected")
    $(parent_card).addClass("selected")
    var selectedCanvasObj = canvas.getObjects().filter(i => i.canvasId == guid)[0]
    canvas.setActiveObject(selectedCanvasObj)
    canvas.renderAll()
})

$(window).resize(function () {
    var maxImageHeight = ($(window).height() / 100) * 60;
    $(".dvParentCanvas").css({
        "max-height": (imageHeight > maxImageHeight ? maxImageHeight : imageHeight) + "px",
        "max-width": imageWidth + "px"
    })
});

document.addEventListener('touchstart', function (e) {
    console.log(e);
});

$(document).on("input", ".txtColor", function () {
    // debugger
    var color = ($(this).val())
    $.each(canvas.getObjects(), function (index, obj) {
        if (index > 0) {
            obj.set("stroke" , color);
            canvas.renderAll()
        }
    });
})

document.onkeydown = KeyPress;
canvas.on('object:removed', function (opt) {
    if (opt.target.canvasId) {
        if (canvas.getObjects().filter(i => i.canvasId == opt.target.canvasId).length > 0) {
            var removableObj = canvas.getObjects().filter(i => i.canvasId == opt.target.canvasId)
            canvas.getObjects().filter(i => i.canvasId == opt.target.canvasId).forEach(function (obj) {
                canvas.remove(obj);
            })
            canvas.renderAll();
        }
        if (!$("#" + opt.target.canvasId).hasClass("d-none")) {
            $("#" + opt.target.canvasId).addClass("d-none")
        }
    }
})

canvas.on('object:added', function (opt) {
    if (opt.target.canvasId) {
        if ($("#" + opt.target.canvasId).length > 0) {
            if ($("#" + opt.target.canvasId).hasClass("d-none")) {
                $("#" + opt.target.canvasId).removeClass("d-none")
            }
        }
    }
})

canvas.on('mouse:wheel', function (opt) {
    if (enableZoom) {
        var delta = opt.e.deltaY;
        var zoom = canvas.getZoom();
        zoom *= 0.999 ** delta;
        if (zoom > 20) zoom = 20;
        if (zoom < 0.01) zoom = 0.01;
        canvas.setWidth(imageWidth * zoom);
        canvas.setHeight(imageHeight * zoom);
        canvas.setViewportTransform([zoom, 0, 0, zoom, 0, 0]);
        canvas.zoomToPoint({ x: opt.e.offsetX, y: opt.e.offsetY }, zoom);
        opt.e.preventDefault();
        opt.e.stopPropagation();

    }
});

canvas.on('mouse:down', function (options) {

    mouseDown = true;
    mY = options.e.pageY;
    mX = options.e.pageX;
    if (isRectangleStarted) {
        var mouse = canvas.getPointer(options.e);
        started = true;
        x = mouse.x;
        y = mouse.y;
        var guid = 'canvas_' + CreateGuid()
        var square = new fabric.Rect({
            width: 0,
            height: 0,
            new: 1,
            left: x,
            top: y,
            fill: 'transparent',
            stroke: $('.txtColor').val(),
            strokeWidth: 1,
            canvasId: guid
        }).setCoords();;
        canvas.add(square);
        canvas.renderAll();
        canvas.setActiveObject(square);
    }
    // if (options.target && pointArray.length > 0 && options.target.id == pointArray[0].id) {
    //     generatePolygon(pointArray);
    // }
    else if (polygonMode) {
        addPoint(options);
        if (pointArray.length == 1) {
            startingPolygonPoint = options;
        }
        if (pointArray.length == 4 && startingPolygonPoint) {
            // addPoint(startingPolygonPoint);
            generatePolygon(pointArray);
        }
    }
    else {
        canvas.getObjects()[0].hoverCursor = ""
    }
});

canvas.on('mouse:move', function (options) {
    if (movableImage) {
        canvas.getObjects()[0].hoverCursor = ""
    }
    if (isRectangleStarted) {
        movableImage = false;
        var mouse = canvas.getPointer(options.e);

        var w = Math.abs(mouse.x - x),
            h = Math.abs(mouse.y - y);

        if (!w || !h) {
            return false;
        }

        var square = canvas.getActiveObject();
        if (square) {
            square.set('width', w).set('height', h);
        }
        canvas.renderAll();
    }
    else if (activeLine && activeLine.class == "line") {
        var pointer = canvas.getPointer(options.e);
        activeLine.set({ x2: pointer.x, y2: pointer.y });

        var points = activeShape.get("points");
        points[pointArray.length] = {
            x: pointer.x,
            y: pointer.y
        }
        activeShape.set({
            points: points
        });
        canvas.renderAll();
    }
    canvas.renderAll();
});

canvas.on('mouse:up', function (options) {
    mouseDown = false;
    canvas.getObjects()[0].hoverCursor = "default"
    if (isRectangleStarted) {
        isRectangleStarted = false;
        var square = canvas.getActiveObject();
        if (square) {
            square.on('selected', function (e) {
                CanvasObjectSelected(e);
            });
            $(".annotation_card").removeClass("selected")

            $(".dvAnnotationFields").append(
                get_annotation_template("TEMPORARY", square.canvasId)
            )
            annotationFieldIDs.push(square.canvasId);
        }
    }
})

canvas.on('mouse:dblclick', function (e) {
    if (canvas.getActiveObject() && canvas.getActiveObject().get('type') === "polygon") {
        ToggleEditPolygon(canvas); //double click and polygon; toggels edit polygon points
    }
});

canvas.on('object:moving', function (options) {
    movableImage = false;
    var objType = options.target.get('type');
    if (objType == "circle") {

        var p = options.target;
        $(".annotation_card").removeClass("selected")
        $("#" + p.canvasId).addClass("selected")
        var polygon = canvas.getObjects().filter(i => i.type == "polygon" && i.canvasId == p.canvasId)[0]
        if (polygon) {
            polygon.points[p.name] = { x: p.getCenterPoint().x, y: p.getCenterPoint().y };
            canvas.renderAll();
        }
    }
});

canvas.on('object:scaling', function (options) {
    movableImage = false;
})

function ZoomIn() {
    $(".btnFunction").removeClass("selected")
    $(".btnZoomIn").addClass("selected")
    enableZoom = true;
    // debugger
    canvas.zoomToPoint(new fabric.Point(canvas.width / 2, canvas.height / 2), canvas.getZoom() + 0.1);
    canvas.setWidth(imageWidth * canvas.getZoom() + 0.1);
    canvas.setHeight(imageHeight * canvas.getZoom() + 0.1);
    canvas.setViewportTransform([canvas.getZoom(), 0, 0, canvas.getZoom(), 0, 0]);
}

function ZoomOut() {
    $(".btnFunction").removeClass("selected")
    $(".btnZoomOut").addClass("selected")
    enableZoom = true;
    canvas.zoomToPoint(new fabric.Point(canvas.width / 2, canvas.height / 2), canvas.getZoom() - 0.1);
    canvas.setWidth(imageWidth * canvas.getZoom() - 0.1);
    canvas.setHeight(imageHeight * canvas.getZoom() - 0.1);
    canvas.setViewportTransform([canvas.getZoom(), 0, 0, canvas.getZoom(), 0, 0]);
}
function DefaultZoom() {
    $(".btnFunction").removeClass("selected")
    $(".btnResetZoom").addClass("selected")
    enableZoom = false;
    canvas.setWidth(imageWidth);
    canvas.setHeight(imageHeight);
    canvas.setViewportTransform([1, 0, 0, 1, 0, 0]);
}

function Undo() {
    $(".btnFunction").removeClass("selected")
    $(".btnUndo").addClass("selected")
    if (canvas.getObjects().length > 1) {
        canvas.undo()
    }
}
function Redo() {
    $(".btnFunction").removeClass("selected")
    $(".btnRedo").addClass("selected")
    canvas.redo()
}
function Delete() {

    $(".btnFunction").removeClass("selected")
    $(".btnDelete").addClass("selected")
    // debugger;
    if (canvas.getActiveObject()) {
        canvas.remove(canvas.getActiveObject())
    }
}
function CanvasObjectSelected(e) {
    if (canvas.getActiveObject()) {
        $(".annotation_card").removeClass("selected")
        $("#" + canvas.getActiveObject().canvasId).addClass("selected")
    }
}
function DisableZoom() {
    $(".btnFunction").removeClass("selected")
    $(".btnDisableZoom").addClass("selected")
    enableZoom = false;
}

function CreateGuid() {
    function S4() {
        return (((1 + Math.random()) * 0x10000) | 0).toString(16).substring(1);
    }
    return (S4() + S4() + "-" + S4() + "-4" + S4().substr(0, 3) + "-" + S4() + "-" + S4() + S4() + S4()).toLowerCase();
}

function KeyPress(e) {
    var evtobj = window.event ? event : e;
    if (evtobj.key == "x" && evtobj.ctrlKey) {
        ZoomIn();
    }
    if (evtobj.keyCode == 46) {
        Delete();
    }
    var activeObj = canvas.getActiveObject();
    if (evtobj.keyCode == 37) {
        // left
        if (activeObj && activeObj.type != "circle") {
            activeObj.set("left", activeObj.left - 5)
            canvas.renderAll();
        }
    }
    if (evtobj.keyCode == 38) {
        // up
        if (activeObj && activeObj.type != "circle") {
            activeObj.set("top", activeObj.top - 5)
            canvas.renderAll();
        }
    }
    if (evtobj.keyCode == 39) {
        // right
        if (activeObj && activeObj.type != "circle") {
            activeObj.set("left", activeObj.left + 5)
            canvas.renderAll();
        }
    }
    if (evtobj.keyCode == 40) {
        // down
        if (activeObj && activeObj.type != "circle") {
            activeObj.set("top", activeObj.top + 5)
            canvas.renderAll();
        }
    }
}

function Download() {
    if (canvas.getObjects().length > 0) {
        var result = []
        var pointsArr = []
        var points = []
        for (var i = 0; i < canvas.getObjects().length; i++) {
            // if (canvas.getObjects()[i].type != "image" && canvas.getObjects()[i].new == 1) {
            if (canvas.getObjects()[i].type != "image") {
                points = []
                pointsArr = []
                // var left = canvas.getObjects()[i].left;
                // var top = canvas.getObjects()[i].top;
                // var right = parseFloat(left) + parseFloat(canvas.getObjects()[i].width);
                // var bottom = parseFloat(top) + parseFloat(canvas.getObjects()[i].height);

                // points.push(left)
                // points.push(top)
                // pointsArr.push(points)
                // points = []
                // points.push(right)
                // points.push(top)
                // pointsArr.push(points)
                // points = []
                // points.push(right)
                // points.push(bottom)
                // pointsArr.push(points)
                // points = []
                // points.push(left)
                // points.push(bottom)
                // pointsArr.push(points)

                // Points order
                // [[left, top], [right, top], [right, bottom], [left, bottom]]
                // i.e
                // [[x0, y0], [x1, y1], [x2, y2], [x3, y3]]

                // pointsArr = [
                //     [left, top],
                //     [right, top],
                //     [right, bottom],
                //     [bottom, right]
                // ]
                // debugger
                
                // TODO: check zoomX ad zoomY properties of canvas if required

                // getting perfect minimal rect value to support polygon -- LineCoords or aCoords
                // 
                let aCoords = canvas.getObjects()[i].aCoords;
                pointsArr = [
                    [aCoords.tl.x, aCoords.tl.y],
                    [aCoords.tr.x, aCoords.tr.y],
                    [aCoords.br.x, aCoords.br.y],
                    [aCoords.bl.x, aCoords.bl.y]
                ]

                var txtValue = $("#" + canvas.getObjects()[i].canvasId).find(".txtRecognize").val()
                result.push({
                    "transcription": txtValue,
                    "points": pointsArr,
                    "canvasId": canvas.getObjects()[i].canvasId
                });
                
            }
        }

        // console.log(JSON.stringify(result))
        console.log("result : ", result)

        // send word annotation data to server via ajax
        let sendData = []
        for(let i = 0; i<result.length; i++){
            let temp = {};
            temp['word_index'] = i+1;

            // let parentDiv = document.getElementById(`${annotationFieldIDs[i]}`);
            let parentDiv = document.getElementById(`${result[i]["canvasId"]}`);
            temp['text'] = parentDiv.querySelector("#text").value;
            temp['lang_id'] = parseInt(parentDiv.querySelector("#lang").value);
            temp['font_id'] = parseInt(parentDiv.querySelector("#font").value);
            temp['is_bold'] = parentDiv.querySelector("#check1").checked;
            temp['is_italic'] = parentDiv.querySelector("#check2").checked;
            temp['task_id'] = parseInt(taskID);
            temp['box_coordinates'] = result[i].points;
            // console.log(temp);
            sendData.push(temp);
        }
        console.log("sendData: ", sendData);

        //ajax communication 
        $.ajax({
            url: "/annotate/save-wordannotate-data",
            type: "POST",
            data: { 
                csrfmiddlewaretoken: $("#csrfid").val(),
                sendData: JSON.stringify(sendData)
            }, 
            success: function (response) {
                
                alert('success');
            },
            error: function (response) {

                alert('error');
            },
        });
        //end ajax
        // end send annotation data

        // downlaod annotation 
        // var a = document.createElement("a");
        // a.href = canvas.toDataURL()
        // a.download = "Image.png";
        // a.click();
    }
}

function drawPolygon() {
    if (canvas.getObjects().length > 0 && polygonMode == false) {
        polygonMode = true;
        pointArray = new Array();
        lineArray = new Array();
        activeLine;
        startingPolygonPoint;
    }
};

function addPoint(options) {
    var random = Math.floor(Math.random() * (max - min + 1)) + min;
    var id = new Date().getTime() + random;
    var circle = new fabric.Circle({
        radius: 5,
        fill: '#ffffff',
        stroke: $('.txtColor').val(),
        strokeWidth: 0.5,
        left: (options.e.layerX / canvas.getZoom()),
        top: (options.e.layerY / canvas.getZoom()),
        selectable: true,
        hasBorders: false,
        hasControls: false,
        originX: 'center',
        originY: 'center',
        id: id,
        objectCaching: false
    });
    if (pointArray.length == 0) {
        circle.set({
            fill: $('.txtColor').val()
        })
    }
    circle.on('selected', function (e) {
        CanvasObjectSelected(e);
    });

    var points = [
        (options.e.layerX / canvas.getZoom()),
        (options.e.layerY / canvas.getZoom()),
        (options.e.layerX / canvas.getZoom()),
        (options.e.layerY / canvas.getZoom())
    ];

    line = new fabric.Line(points, {
        strokeWidth: 2,

        stroke: $('.txtColor').val(),
        class: 'line',
        originX: 'center',
        originY: 'center',
        selectable: false,
        hasBorders: false,
        hasControls: false,
        evented: false,
        objectCaching: false
    });

    if (activeShape) {
        var pos = canvas.getPointer(options.e);
        var points = activeShape.get("points");
        points.push({
            x: pos.x,
            y: pos.y
        });
        var polygon = new fabric.Polygon(points, {
            stroke: '#333333',
            strokeWidth: 1,
            opacity: 0.3,
            selectable: false,
            hasBorders: false,
            hasControls: false,
            evented: false,
            objectCaching: false
        });
        canvas.remove(activeShape);
        canvas.add(polygon);
        activeShape = polygon;
        canvas.renderAll();
    }
    else {
        var polyPoint = [{
            x: (options.e.layerX / canvas.getZoom()),
            y: (options.e.layerY / canvas.getZoom())
        }];
        var polygon = new fabric.Polygon(polyPoint, {
            stroke: '#333333',
            strokeWidth: 1,
            opacity: 0.3,
            selectable: false,
            hasBorders: false,
            hasControls: false,
            evented: false,
            objectCaching: false
        });
        activeShape = polygon;
        canvas.add(polygon);
    }
    activeLine = line;

    pointArray.push(circle);
    lineArray.push(line);

    canvas.add(line);
    canvas.add(circle);
    canvas.selection = false;
};

function generatePolygon(pointArray) {
    var points = new Array();
    var guid = 'canvas_' + CreateGuid()
    $.each(pointArray, function (index, point) {
        points.push({
            x: point.left,
            y: point.top
        });
        point.canvasId = guid;
        point.name = index;
        canvas.remove(point);
    });
    $.each(lineArray, function (index, line) {
        canvas.remove(line);
    });
    canvas.remove(activeShape).remove(activeLine);

    var polygon = new fabric.Polygon(points, {
        stroke: $('.txtColor').val(),
        strokeWidth: 0.5,
        fill: 'transparent',
        opacity: 1,
        selectable: true,
        objectCaching: false,
        hasBorders: false,
        hasControls: true,
        canvasId: guid,
        edit: false
    });
    canvas.add(polygon);
    polygon.on('selected', function (e) {
        CanvasObjectSelected(e);
    });
    $(".annotation_card").removeClass("selected")

    $(".dvAnnotationFields").append(
        get_annotation_template("TEMPORARY", guid)
    );
    activeLine = null;
    activeShape = null;
    polygonMode = false;
    canvas.selection = true;
}


function ToggleEditPolygon(canvas) {
    var poly = canvas.getActiveObject();
    canvas.setActiveObject(poly);
    poly.edit = !poly.edit;
    //if (poly.edit) {
    var lastControl = poly.points.length - 1;
    poly.hasBorders = false;
    poly.cornerStyle = 'circle';
    poly.cornerColor = 'rgba(0,0,255,0.5)';
    poly.controls = poly.points.reduce(function (acc, point, index) {
        acc['p' + index] = new fabric.Control({
            positionHandler: polygonPositionHandler,
            actionHandler: anchorWrapper(index > 0 ? index - 1 : lastControl, actionHandler),
            actionName: 'modifyPolygon',
            pointIndex: index
        });
        return acc;
    }, {});
    // } else {
    //     poly.cornerStyle = 'rect';
    //     poly.controls = fabric.Object.prototype.controls;
    // }
    //poly.hasBorders = !poly.edit;
    canvas.requestRenderAll();
}

function actionHandler(eventData, transform, x, y) {
    movableImage = false;
    var polygon = transform.target,
        currentControl = polygon.controls[polygon.__corner],
        mouseLocalPosition = polygon.toLocalPoint(new fabric.Point(x, y), 'center', 'center'),
        polygonBaseSize = getObjectSizeWithStroke(polygon),
        size = polygon._getTransformedDimensions(0, 0),
        finalPointPosition = {
            x: mouseLocalPosition.x * polygonBaseSize.x / size.x + polygon.pathOffset.x,
            y: mouseLocalPosition.y * polygonBaseSize.y / size.y + polygon.pathOffset.y
        };
    polygon.points[currentControl.pointIndex] = finalPointPosition;
    return true;
}

function anchorWrapper(anchorIndex, fn) {
    return function (eventData, transform, x, y) {
        var fabricObject = transform.target,
            absolutePoint = fabric.util.transformPoint({
                x: (fabricObject.points[anchorIndex].x - fabricObject.pathOffset.x),
                y: (fabricObject.points[anchorIndex].y - fabricObject.pathOffset.y),
            }, fabricObject.calcTransformMatrix()),
            actionPerformed = fn(eventData, transform, x, y),
            newDim = fabricObject._setPositionDimensions({}),
            polygonBaseSize = getObjectSizeWithStroke(fabricObject),
            newX = (fabricObject.points[anchorIndex].x - fabricObject.pathOffset.x) / polygonBaseSize.x,
            newY = (fabricObject.points[anchorIndex].y - fabricObject.pathOffset.y) / polygonBaseSize.y;
        fabricObject.setPositionByOrigin(absolutePoint, newX + 0.5, newY + 0.5);
        return actionPerformed;
    }
}

function getObjectSizeWithStroke(object) {
    var stroke = new fabric.Point(
        object.strokeUniform ? 1 / object.scaleX : 1,
        object.strokeUniform ? 1 / object.scaleY : 1
    ).multiply(object.strokeWidth);
    return new fabric.Point(object.width + stroke.x, object.height + stroke.y);
}

function polygonPositionHandler(dim, finalMatrix, fabricObject) {
    var x = (fabricObject.points[this.pointIndex].x - fabricObject.pathOffset.x),
        y = (fabricObject.points[this.pointIndex].y - fabricObject.pathOffset.y);
    return fabric.util.transformPoint(
        { x: x, y: y },
        fabric.util.multiplyTransformMatrices(
            fabricObject.canvas.viewportTransform,
            fabricObject.calcTransformMatrix()
        )
    );
}
function addImageInCanvas(imagepath) {
    fabric.Image.fromURL(imagepath, function (img) {
        canvas.clear();
        $(".dvAnnotationFields").html('')
        // $("#CanvasModalLabel").text(e.target.files[0].name)
        imageHeight = img.height;
        imageWidth = img.width;
        img.set({
            originX: 'left',
            originY: 'top',
            objectCaching: false,
            fill: 'transparent',
            selectable: false,
            type: "image"
        });
        canvas.setHeight(img.height);
        canvas.setWidth(img.width);

        canvas.add(img).renderAll();
    });
}



///Preview
function Preview(){
    if(canvas.getObjects().length > 0){

        var taskPreviewAnnotations=[];
        if(localStorage.getItem("taskAnnotations")!=null)
            taskPreviewAnnotations=JSON.parse(localStorage.getItem("taskAnnotations"))
        var taskId = $('#frmTask').val();    
        taskPreviewAnnotations =taskPreviewAnnotations.filter(i=>i.task!=taskId);   
        //var form = new FormData()
        for (var i = 0; i < canvas.getObjects().length; i++) {
            if (canvas.getObjects()[i].type != "image" && $("#"+canvas.getObjects()[i].canvasId).is(":visible")) {
                taskPreviewAnnotations.push({
                    "task":$('#frmTask').val(),
                    "text" : $("#"+canvas.getObjects()[i].canvasId+" .txtRecognize").val(),
                    "lang" : $("#"+canvas.getObjects()[i].canvasId+" .ddlLanguage").val(),
                    "font" : $("#"+canvas.getObjects()[i].canvasId+" .ddlFont").val(),
                    "isBold" : $("#"+canvas.getObjects()[i].canvasId+" .chkIsBold").is(":checked"),
                    "isItalic" : $("#"+canvas.getObjects()[i].canvasId+" .chkIsItalic").is(":checked"),
                    "left" : canvas.getObjects()[i].left,
                    "top" :canvas.getObjects()[i].top,
                    "height" :canvas.getObjects()[i].height,
                    "width" :canvas.getObjects()[i].width,
                    "color": $("#"+canvas.getObjects()[i].canvasId+" .txtColor").val(),
                    "canvasId":canvas.getObjects()[i].canvasId
                })
              
            }
        }
        // form.append("annottions" ,taskPreviewAnnotations);
        // $.ajax({
        //     type: "POST",
        //     url: "{{ url 'save_annotations'}}",   
        //     data:form,   /* Passing the text data */
        //     success:  function(response){
        //            alert(response);
        //        },
        //     error: function(){
        //         alert("error save annotation")
        //     }   
        // });

       
        var frmdata =JSON.stringify(taskPreviewAnnotations);
        console.log("form data")
        console.log(frmdata)
        localStorage.setItem("taskAnnotations",frmdata);
        console.log(taskPreviewAnnotations)

//         addImageInPreviewCanvas($(".hdfImgPath").val())
//         //add updates text changes in preview canvas
//         setTimeout(function(){
//             for (var i = 0; i < taskPreviewAnnotations.length; i++) {
//                 AddTextForPreviewCanvas(taskPreviewAnnotations[i])
//             }   
//         },500)
       
// $(".dvPreview").show()
// $(".dvMain").hide()
location.href="/annotate/preview";
    }
}


// function addImageInPreviewCanvas(imagepath) {
//     fabric.Image.fromURL(imagepath, function (img) {
//         previewCanvas.clear();  
//         img.set({
//             originX: 'left',
//             originY: 'top',
//             objectCaching: false,
//             fill: 'transparent',
//             selectable: false,
//             type: "image",
//             opacity:0.5
//         });
//         previewCanvas.setHeight(img.height);
//         previewCanvas.setWidth(img.width); 
//         previewCanvas.add(img).renderAll();
//     });
// }


// function AddTextForPreviewCanvas(renderObj) {
   
//     var obj = new fabric.IText(renderObj.text, {
//         left: renderObj.left,
//         top: renderObj.top,
//         fontFamily: 'arial',
//         fill: renderObj.color,
//         fontSize: 16, 
//         fontWeight: renderObj.isBold==true?'bold':'normal',
//         fontStyle: renderObj.isItalic==true?'italic':'normal',
//         canvasId: renderObj.canvasId,
//         selectable: true,
//         crossOrigin: 'anonymous',
//         originX: 'left', originY: 'top',
//     });
//     previewCanvas.add(obj) 
//     previewCanvas.setActiveObject(obj); 
//     // AddAnnotationToTimeline(n, 0, max, "Text here")
//     previewCanvas.renderAll();
   
// }


function CancelPreview(){
    $(".dvPreview").hide()
    $(".dvMain").show()
}