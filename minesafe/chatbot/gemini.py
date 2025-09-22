import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Initialize Gemini model
model = ChatGoogleGenerativeAI(
    model="models/gemini-2.5-flash",
    google_api_key=GOOGLE_API_KEY
)

# Initialize a fresh chat history
def init_chat():
    return [
        SystemMessage(
            content=(
                "You are RockGuard — a concise, safety-first assistant for open-pit mine operations. "
                "Always confirm user intent. Tone: calm, clear, and practical."
            )
        )
    ]

# Chat function
def chat_gemini(user_input, chat_history):
    chat_history.append(HumanMessage(content=user_input))
    result = model.invoke(chat_history)
    chat_history.append(AIMessage(content=result.content))
    return result.content, chat_history
