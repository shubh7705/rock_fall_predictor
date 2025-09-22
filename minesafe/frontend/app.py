import streamlit as st
import requests

# Backend API base URL
BACKEND_URL = "http://127.0.0.1:8000"   # change if deployed

# Session state to persist chat session id & messages
if "session_id" not in st.session_state:
    st.session_state.session_id = None
if "messages" not in st.session_state:
    st.session_state.messages = []


# Function to start a new session
def start_session():
    response = requests.post(f"{BACKEND_URL}/start_chat/")
    if response.status_code == 200:
        data = response.json()
        st.session_state.session_id = data["session_id"]
        st.session_state.messages = []
        st.success("✅ New chat session started!")
    else:
        st.error("❌ Failed to start chat session")


# Function to send a message
def send_message(user_input):
    if not st.session_state.session_id:
        st.warning("Start a chat session first.")
        return

    payload = {"message": user_input}
    response = requests.post(
        f"{BACKEND_URL}/chat_with_gemini/{st.session_state.session_id}/",
        json=payload
    )

    if response.status_code == 200:
        data = response.json()
        ai_response = data["response"]

        # Store messages in session state
        st.session_state.messages.append(("You", user_input))
        st.session_state.messages.append(("RockGuard", ai_response))
    else:
        st.error("❌ Failed to get response from backend")


# Streamlit UI
st.title("🪨 RockGuard - Open-Pit Mine Safety Chatbot")

if st.button("Start New Chat"):
    start_session()

# Display chat history
for role, msg in st.session_state.messages:
    if role == "You":
        st.chat_message("user").markdown(msg)
    else:
        st.chat_message("assistant").markdown(msg)

# Input box at the bottom
if prompt := st.chat_input("Ask RockGuard..."):
    send_message(prompt)
