
let imageFile = document.getElementById("inputfile");

// let imageFile = document.getElementById("inputFile");

let form = document.getElementById("formForEst")
let imageElem = document.getElementById("imageToEst");


let uploadButton = document.getElementById("uploadButton");

let modelEstResult = document.getElementById("modelSays");

// Allows us to convert uploaded group image to string
const toBase64 = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
});

form.addEventListener("submit", async (event)=>{
    console.log("YO")
    let image = imageFile.files[0];
    // e.preventDefault();
    imgData = await toBase64(image);
    localStorage.setItem("imgData", imgData);
    imageElem.src = imageFile.files[0];
});


if(localStorage.getItem("imgData")!== null){
    imageElem.src = localStorage.getItem("imgData");
}

else{
    imageElem.src = "static/4036626958.jpg";
}


let playGameButton = document.getElementById("playGameButton");

playGameButton.addEventListener("click", async (event)=>{
    console.log("YO")
    try {

        window.location.href = '/gamePage';
            }
    catch (err) {
        console.log("error")

        throw Error(`Unexpected error: ${err}`);
    }
});