//Asynch function that corrospondes with the onClick event
//Once a click is made the function will analyze the users input and then grab everything from the live backend on render
//It uses the anyanlysis get route to publish everything to the front page.
async function submitResponse() {
  const userInput = document.getElementById('userInput').value;
  const resultElement = document.getElementById('result');

  try {
    const response = await fetch('https://philosophy-ai.onrender.com/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ response: userInput })
    });
      //Asynch Function for error cathcing once analysis is made
    const data = await response.json();

    if (response.ok) {
      resultElement.innerText = data.analysis;
    } else {
      resultElement.innerText = "Error: " + (data.error || 'Something went wrong.');
      console.error("Server returned an error:", data);
    }
  } catch (error) {
    resultElement.innerText = "Network error: " + error.message;
    console.error("Network or server error:", error);
  }
}
 async function generateDilemma(){
  const dilemmaElelment = document.getElememntById('dilemma');
  try {
    const response = await fetch('https://philosophy-ai.onrender.com/generate-dilemma');
    const data = await response.json();

    if (response.ok) {
      dilemmaElelment.innerText = data.dilemma;
    } else {
      dilemmaElelment.innerText = "Error: " + (data.error || 'Something went wrong.');
      console.error("Server returned an error:", data);
    }
  } catch (error) {
    dilemmaElelment.innerText = "Network error: " + error.message;
    console.error("Network or server error:", error);
  }
 }