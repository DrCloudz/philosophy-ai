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
