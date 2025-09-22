from django.urls import path
from . import views

urlpatterns = [
    path("start_chat/", views.start_chat, name="start_chat"),
    path("chat_with_gemini/<uuid:session_id>/", views.chat_with_gemini, name="chat_with_gemini"),
]
