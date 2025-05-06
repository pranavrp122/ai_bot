document.getElementById('send-button').addEventListener('click', async () => {
    const userInput = document.getElementById('user-input').value;
    const responseArea = document.getElementById('response-area');
    const audioPlayer = document.getElementById('audio-player');
    const avatarVideo = document.getElementById('avatar-video');

    if (!userInput) {
        responseArea.textContent = "Please enter a message.";
        return;
    }

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userInput })
        });

        const data = await response.json();

        if (data.response) {
            responseArea.textContent = `AI: ${data.response}`;
            
            // Play audio response if available
            if (data.audio_file) {
                audioPlayer.src = `/${data.audio_file}`;
                audioPlayer.style.display = "block";
                audioPlayer.play();
            }

            // Play video response if available
            if (data.video_url) {
                avatarVideo.src = data.video_url;
                avatarVideo.style.display = "block";
                avatarVideo.play();
            }
        } else {
            responseArea.textContent = `Error: ${data.error}`;
        }
    } catch (error) {
        responseArea.textContent = `Error: ${error.message}`;
    }
});
