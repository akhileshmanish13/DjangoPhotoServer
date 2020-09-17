
function loadImageIntoFrame(){
    console.log("loading ImageIntoFrame 0");
    var img = document.createElement("img"); 
    
    img.src = "./newPic"; 
    var imageFrame = document.getElementById("photoFrame"); 
    
    src.appendChild(img);
}



function loadImageIntoFrame(){
    console.log("loading ImageIntoFrame ");
    
    var imageFrame = document.getElementById("photoFrame"); 
    imageFrame.src = "./newPic"; 
}

console.log("Executing JS");

loadImageIntoFrame();
const interval = setInterval(loadImageIntoFrame, 1000);
 //  clearInterval(interval); // thanks @Luca D'Amico