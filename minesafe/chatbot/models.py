from django.db import models
import uuid


class ChatSession(models.Model):
    """Each chat session (no user authentication required)."""
    session_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ChatSession {self.session_id}"


class ChatMessage(models.Model):
    """Stores messages in a session."""
    ROLE_CHOICES = (
        ("system", "System"),
        ("human", "Human"),
        ("ai", "AI"),
    )

    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.role}] {self.content[:50]}"
