function updateBackgroundPhotoFrame(frameNumber){

    var imageFrame = document.getElementById("photoFrame"+frameNumber);
    imageFrame.src = '';
    imageFrame.src = './newPic?'+ new Date().getTime();//Forces a reload of the new picture

}

function hideForegroundPhotoFrame(frameNumber){
    frameNumber=2
    className = "hiddenPhotoFrame"
    var imageFrame = document.getElementById("photoFrame"+frameNumber);

    if(imageFrame.classList.contains(className)){
        imageFrame.classList.remove(className)
    }else{
        imageFrame.classList.add(className)
    }

}


function backgroundPhotoFrame(){
    if(currentPhotoFrame == 1){
        return 2
    }
    else{
        return 1
    }
}

function loadImageIntoFrame(){
    console.log("loading ImageIntoFrame ");

    updateBackgroundPhotoFrame(backgroundPhotoFrame())

    // Wait for the background of the other to actually load - other it will load and pop halfway through the fade-transition
    setTimeout(function(){

        hideForegroundPhotoFrame(currentPhotoFrame);
        currentPhotoFrame = backgroundPhotoFrame();

        // Call self again!
        // setTimeout(loadImageIntoFrame(), waitForLoadMs);
        loadImageIntoFrame()
    }, waitForLoadMs);

    refreshCount+=1;
    if(refreshCount >= reloadPageAfterThisManyImages){
        console.log("refreshCount=", refreshCount, " reloadPageAfterThisManyImages: ", reloadPageAfterThisManyImages);
        location.reload();
    }
}


var currentPhotoFrame = 1;
var refreshCount = 0;

var waitForLoadMs = 3000;
var reloadPageAfterThisManyImages = 20

loadImageIntoFrame();

function openFullscreen(){

    var elem = document.getElementById("photoframe_container");

    if (elem.requestFullscreen) {
        elem.requestFullscreen();
      } else if (elem.mozRequestFullScreen) { /* Firefox */
        elem.mozRequestFullScreen();
      } else if (elem.webkitRequestFullscreen) { /* Chrome, Safari and Opera */
        elem.webkitRequestFullscreen();
      } else if (elem.msRequestFullscreen) { /* IE/Edge */
        elem.msRequestFullscreen();
      }
}
