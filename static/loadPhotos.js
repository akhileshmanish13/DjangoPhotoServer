function updateBackgroundPhotoFrame(frameNumber){

    var imageFrame = document.getElementById("photoFrame"+frameNumber);
    imageFrame.src = '';
    imageFrame.src = './newPic?'+ new Date().getTime();//Forces a reload of the new picture

}

function hideForegroundPhotoFrame(){
    
    var imageFrame = document.getElementById("photoFrameForeground");

    className = "hiddenPhotoFrame"
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
    console.log("loading new ImageIntoFrame");

    updateBackgroundPhotoFrame(backgroundPhotoFrame())

    // Wait for the background of the other to actually load - other it will load and pop halfway through the fade-transition
    setTimeout(function(){

        hideForegroundPhotoFrame();
        currentPhotoFrame = backgroundPhotoFrame();

        loadImageIntoFrame(); // Call self again!
    }, waitForLoadMs);

    refreshCount+=1;
    if(refreshCount >= reloadPageAfterThisManyImages){
        console.log("refreshCount=", refreshCount, " reloadPageAfterThisManyImages: ", reloadPageAfterThisManyImages);
        location.reload();
    }
}


var currentPhotoFrame = 1;
var refreshCount = 0;  //reload the page after this many files so that the browser can cleanup  memory.

var waitForLoadMs = 10  *1000;
var reloadPageAfterThisManyImages = 20

loadImageIntoFrame();
