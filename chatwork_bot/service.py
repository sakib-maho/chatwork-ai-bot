"""Lightweight Chatwork API client abstraction (mock-friendly)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


class ChatworkClient(Protocol):
    def send_message(self, room_id: str, body: str) -> dict:
        ...


@dataclass
class InMemoryChatworkClient:
    """Test double that stores outbound messages."""

    sent: list[dict[str, str]] = field(default_factory=list)

    def send_message(self, room_id: str, body: str) -> dict:
        payload = {"room_id": room_id, "body": body}
        self.sent.append(payload)
        return {"ok": True, **payload}


@dataclass
class BotService:
    client: ChatworkClient

    def handle_incoming(self, room_id: str, text: str) -> dict:
        from .responder import build_rich_response

        result = build_rich_response(text, room=room_id)
        self.client.send_message(room_id, str(result["response"]))
        return result
