from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from datetime import datetime

app = Flask(__name__)

# Configure the Gemini API
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("The GOOGLE_API_KEY environment variable is not set.")

genai.configure(api_key=api_key)

chat_history = []

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', chat_history=chat_history)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json['user_input']
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    chat_history.append({"role": "user", "content": user_input, "timestamp": timestamp})
    
    # Generate AI response using Gemini API
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = (
        f"Respond to the following user input: '{user_input}'\n"
        "Provide a concise response with the following guidelines:\n"
        "1. Start with a brief, empathetic acknowledgment.\n"
        "2. Give 3 short, practical suggestions, each in 1-2 sentences.\n"
        "3. Format the response with numbered points.\n"
        "4. Add a brief reminder about seeking professional help if needed.\n"
        "5. Keep the entire response friendly and under 150 words."
    )
    
    response = model.generate_content(prompt)
    ai_response = response.text
    
    chat_history.append({"role": "ai", "content": ai_response, "timestamp": timestamp})
    
    return jsonify({"ai_response": ai_response, "timestamp": timestamp})

if __name__ == '__main__':
    app.run(debug=True)