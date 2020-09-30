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
        
        // Foreground takes about 2.5s to hide, so need to reload AFTER that.
        setTimeout(loadImageIntoFrame, 2500);
    }, waitForLoadMs);

    refreshCount+=1;
    if(refreshCount >= reloadPageAfterThisManyImages){
        console.log("refreshCount=", refreshCount, " reloadPageAfterThisManyImages: ", reloadPageAfterThisManyImages);
        location.reload();
    }
}


var currentPhotoFrame = 2;
var refreshCount = 0;  //reload the page after this many files so that the browser can cleanup  memory.

var waitForLoadMs = 10  *1000;



// https://davidwalsh.name/query-string-javascript
function getUrlParameter(name) {
    name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
    var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
    var results = regex.exec(location.search);
    return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
};

var reloadPageAfterThisManyImages = 20

if( getUrlParameter('light') ){

    reloadPageAfterThisManyImages = getUrlParameter('light')
    if( isNaN(reloadPageAfterThisManyImages) ){
	reloadPageAfterThisManyImages = 6
    }
    
}
    
console.log("reloadPageAfterThisManyImages: ", reloadPageAfterThisManyImages)


// Will recursively call itself.
loadImageIntoFrame();
