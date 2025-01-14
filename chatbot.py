import openai
from flask import Flask, request, jsonify, render_template
from gtts import gTTS

import os

app = Flask(__name__)

# OpenAI API Key (replace with your actual key)
openai.api_key = "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"

# Route for Chatbot Responses
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    try:
        # Generate AI response
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_input}]
        )
        ai_response = response['choices'][0]['message']['content']

        # Convert response to speech
        tts = gTTS(ai_response)
        audio_file = "response.mp3"
        tts.save(audio_file)

        return jsonify({"response": ai_response, "audio_file": audio_file})
    except openai.error.OpenAIError as e:
        return jsonify({"error": f"OpenAI API error: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
