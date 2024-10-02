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

# GitHub repository URL
github_url = "https://github.com/Ojhaharsh/mental-health-chatbot"

# Create two columns for the top section
col1, col2 = st.columns([3, 1])

with col1:
    # Add "Star on GitHub" button
    st.markdown(f"[![Star on GitHub](https://img.shields.io/github/stars/Ojhaharsh/mental-health-chatbot.svg?style=social)]({github_url})")

with col2:
    # Add the footer right beneath the star button
    st.markdown(
        """
        <div style="font-size: 0.8em; text-align: right;">
        Made with ❤️ by <strong>BuilderBabu</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

st.title("Mental Health Chatbot")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

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
        f"You are a mental health support chatbot. Respond to the following user input: '{user_input}'\n"
        "Provide a concise, contextually appropriate response with the following guidelines:\n"
        "1. Start with a brief, empathetic acknowledgment of the user's input.\n"
        "2. If appropriate, give 1-2 short, practical suggestions related to the user's concern.\n"
        "3. Keep the response friendly and under 50 words.\n"
        "4. Only mention professional help if the user's message indicates severe distress."
    )
       
    response = model.generate_content(prompt)
    ai_response = response.text
       
    # Add AI response to chat history
    st.session_state.chat_history.append({"role": "ai", "content": ai_response, "timestamp": timestamp})
       
    # Display the AI response
    with st.chat_message("ai"):
        st.write(f"{timestamp}: {ai_response}")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.write(f"{message['timestamp']}: {message['content']}")
#Add a button to clear chat history
if st.button("Clear Chat History"):
    st.session_state.chat_history = []
    st.rerun()

