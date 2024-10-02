import streamlit as st
import os
import google.generativeai as genai
from datetime import datetime

# Configure the Gemini API
api_key = st.secrets.get("GOOGLE_API_KEY") or os.environ.get("GOOGLE_API_KEY")
if not api_key:
    st.error("The GOOGLE_API_KEY is not set in secrets or environment variables.")
    st.stop()

genai.configure(api_key=api_key)

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("Mental Health Chatbot")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(f"{message['timestamp']}: {message['content']}")

# User input
user_input = st.chat_input("What's on your mind?")

if user_input:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input, "timestamp": timestamp})
    
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
    
    # Add AI response to chat history
    st.session_state.chat_history.append({"role": "ai", "content": ai_response, "timestamp": timestamp})
    
    # Display the AI response
    with st.chat_message("ai"):
        st.write(f"{timestamp}: {ai_response}")

# Optional: Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.experimental_rerun()