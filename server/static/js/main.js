
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

// uploadButton.addEventListener("click", async (event)=>{
//     // let imageString = await toBase64(imageFile.files[0]);
//     imageElem.src = imageString;
//     let estimate = await getEstimate(imageString);
//     modelEstResult.innerHTML = estimate;
// });


// async function getEstimate(imageString){
//     try {
//         const response = await fetch(`/`, {
//             method: 'POST',
//             headers: {
//                 "Content-Type": "application/json",
//               },
//             body: JSON.stringify({imageString: imageString})
//         });
    
//         // await handleResponseStatus(response);
    
//         const data = await response.json();
//         console.log(data);
//         return data.estimated_year;
//     }
//     catch (err) {
//         throw Error(`Unexpected error: ${err}`);
//     }
// }

if(localStorage.getItem("imgData")!== null){
    imageElem.src = localStorage.getItem("imgData");
}

else{
    imageElem.src = "static/4036626958.jpg";
}
