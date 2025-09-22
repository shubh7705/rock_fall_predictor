import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import ChatSession, ChatMessage
from .gemini import chat_gemini, init_chat
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage


@csrf_exempt
def start_chat(request):
    """
    Creates a new chat session (no user login required).
    """
    if request.method == "POST":
        session = ChatSession.objects.create()

        # Add system message at start
        system_messages = init_chat()
        for msg in system_messages:
            ChatMessage.objects.create(session=session, role="system", content=msg.content)

        return JsonResponse({"session_id": str(session.session_id), "message": "Chat session started."})


@csrf_exempt
def chat_with_gemini(request, session_id):
    """
    Handles chatting within an existing session.
    """
    if request.method == "POST":
        data = json.loads(request.body)
        user_input = data.get("message")

        try:
            session = ChatSession.objects.get(session_id=session_id)
        except ChatSession.DoesNotExist:
            return JsonResponse({"error": "Session not found."}, status=404)

        # Build chat history for Gemini
        chat_history = []
        for msg in session.messages.all().order_by("timestamp"):
            if msg.role == "system":
                chat_history.append(SystemMessage(content=msg.content))
            elif msg.role == "human":
                chat_history.append(HumanMessage(content=msg.content))
            elif msg.role == "ai":
                chat_history.append(AIMessage(content=msg.content))

        # Add new user input
        response, updated_history = chat_gemini(user_input, chat_history)

        # Save human + AI message in DB
        ChatMessage.objects.create(session=session, role="human", content=user_input)
        ChatMessage.objects.create(session=session, role="ai", content=response)

        return JsonResponse({"response": response})
