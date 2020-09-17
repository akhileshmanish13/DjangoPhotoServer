function updateBackgroundPhotoFrame(frameNumber){

    var imageFrame = document.getElementById("photoFrame"+frameNumber); 
    imageFrame.style.backgroundImage = "url('')"; 
    imageFrame.style.backgroundImage = "url('./newPic')";//Forces a reload of the new one

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
        setTimeout(loadImageIntoFrame, photoRefreshRate);
    }, waitForLoadMs);
    
}


var currentPhotoFrame = 2;


var waitForLoadMs = 2000;
var photoRefreshRate = 5000; 

loadImageIntoFrame();