import openai
import requests
from flask import Flask, request, jsonify, render_template
from gtts import gTTS
import os
import time

app = Flask(__name__)

# OpenAI API Key
openai.api_key = openai_api


# D-ID API Key
d_id_api_key = d_id_api

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        # Generate AI response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        ai_response = response['choices'][0]['message']['content'].strip()

        # Convert response to speech
        audio_file = "static/audio/response.mp3"
        tts = gTTS(ai_response)
        tts.save(audio_file)




        # Generate video using D-ID API
        d_id_url = "https://api.d-id.com/talks"
        headers = {
            "Authorization": f"Basic {d_id_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "source_url": "https://img.freepik.com/free-photo/good-looking-caucasian-female-with-blonde-straight-hair-wearing-glasses-denim-shirt-smiles-happily-has-good-mood-after-successful-day-university-glad-pleased-pose_176420-13174.jpg?t=st=1736876218~exp=1736879818~hmac=212c12698ae8c7c660a954d3c06bd807bb473a830baf0d5835a0ff1f9b784849&w=1480",  # Replace with your avatar's video URL
            "script": {
                "type": "text",
                "input": ai_response
            },
            "config": {
                "stitch": True
            }
        }

        print("Sending POST request to D-ID API...")  # Debugging
        d_id_response = requests.post(d_id_url, headers=headers, json=payload)
        d_id_data = d_id_response.json()
        print("POST Response:", d_id_data)  # Debugging POST response

        # Extract video ID
        video_id = d_id_data.get("id")
        print("Video ID:", video_id)  # Debugging video ID

        if not video_id:
            print("Failed to retrieve video ID.")  # Debugging
            return jsonify({"response": ai_response, "error": "Failed to retrieve video ID"}), 500

        # Polling loop to check video status
        get_video_url = f"https://api.d-id.com/talks/{video_id}"
        print("Polling for video generation status...")  # Debugging
        for attempt in range(10):  # Retry up to 10 times
            print(f"Polling attempt {attempt + 1}...")  # Debugging
            d_id_get_response = requests.get(get_video_url, headers=headers)
            d_id_get_data = d_id_get_response.json()
            print("GET Response:", d_id_get_data)  # Debugging GET response

            video_url = d_id_get_data.get("result_url")
            if video_url:
                print("Video is ready. URL:", video_url)  # Debugging
                return jsonify({"response": ai_response, "video_url": video_url})
            
            print("Video not ready. Retrying in 10 seconds...")  # Debugging
            time.sleep(10)

        # If polling fails to get the result_url
        print("Video generation timed out.")  # Debugging
        return jsonify({"response": ai_response, "error": "Video generation timed out"}), 408

    except openai.OpenAIError as e:
        print("OpenAI API error:", str(e))  # Debugging
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        print("Error:", str(e))  # Debugging
        return jsonify({"error": str(e)}), 500

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


