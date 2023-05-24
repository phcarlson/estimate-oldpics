
let realYears = [1973, 1943, 1968, 1963, 1957, 1986, 1974, 1983];

let yourScoreSoFar = 0;
let modelScoreSoFar = 0;


for (let i = 0; i < 8; i++){
    let button = document.getElementById(`guessButton${i + 1}`);
    let result = document.getElementById(`result${i + 1}`);

    button.addEventListener('click', (event)=>{
        let yourGuess = document.getElementById(`guess${i + 1}`);
        let yourGuessNum = parseFloat(yourGuess.value);
        console.log(yourGuess.value)
        console.log(yourGuessNum);
        if(isNaN(yourGuessNum)){
            console.log("nan")
            alert("Give an actual number thanks");
        }
        else{
            let modelGuess = document.getElementById(`guess${i + 1}Model`);
            let modelGuessNum = parseFloat(modelGuess.value);
            modelGuess.removeAttribute('hidden');
    
            
            if(Math.abs(yourGuessNum - realYears[i]) < Math.abs(modelGuessNum - realYears[i])){
                result.innerText = `Actual year was ${realYears[i]}! YOU WIN THIS ONE. Just give us a week though.`
                result.removeAttribute('hidden');
                yourScoreSoFar += 1;

            }
            else{
                result.innerText = `Actual year was ${realYears[i]}. MODEL WINS THIS ONE. Try harder.`
                result.removeAttribute('hidden');
                modelScoreSoFar += 1;
            }

            
            if(i === 7){
                let result = document.getElementById(`result${i + 1}`);

                let winner = '';
                if(modelScoreSoFar > yourScoreSoFar){
                    winner = "MODEL WINS :(((";
                }
                else if (modelScoreSoFar < yourScoreSoFar){
                    winner = "YOU WIN!!!!"
                }
                else{
                    winner = "You tie. Not sure if that feels good or bad."
                }
                let child = document.createElement('div');
                child.innerHTML = `<b>YOUR FINAL SCORE:</b>${yourScoreSoFar} <br> 
                <b>MODEL'S FINAL SCORE:</b>${modelScoreSoFar} <br> ${winner}`
                result.appendChild(child);
            }
       
        }
    });
}