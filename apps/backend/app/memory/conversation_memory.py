from collections import defaultdict

from app.schemas.conversation import (
    ChatMessage,
)


class ConversationMemory:
    def __init__(self) -> None:
        self.store: dict[
            str,
            list[ChatMessage],
        ] = defaultdict(list)

    def add_message(
        self,
        session_id: str,
        role: str,
        content: str,
    ) -> None:
        self.store[session_id].append(
            ChatMessage(
                role=role,
                content=content,
            )
        )

    def get_messages(
        self,
        session_id: str,
    ) -> list[ChatMessage]:
        return self.store[session_id]

    def clear_session(
        self,
        session_id: str,
    ) -> None:
        self.store[session_id] = []