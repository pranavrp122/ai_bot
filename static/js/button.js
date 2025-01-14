document.getElementById('send-button').addEventListener('click', async () => {
    const userInput = document.getElementById('user-input').value;
    const responseArea = document.getElementById('response-area');
    const audioPlayer = document.getElementById('audio-player');

    if (!userInput) {
        responseArea.textContent = "Please enter a message.";
        return;
    }

    try {
        // Send input to the Flask back end
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userInput })
        });

        const data = await response.json();

        if (data.response) {
            // Display AI response
            responseArea.textContent = `AI: ${data.response}`;
            // Play audio response if available
            if (data.audio_file) {
                audioPlayer.src = `/${data.audio_file}`; // Ensure correct path to the file
                audioPlayer.style.display = "block";
                audioPlayer.play();
            }
        } else {
            responseArea.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        responseArea.textContent = `Error: ${error.message}`;
    }
});
