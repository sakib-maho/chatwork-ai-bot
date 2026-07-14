"""Intent routing and response generation for a local Chatwork-style bot."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable


TOKEN_RE = re.compile(r"[a-z0-9']+")


@dataclass(frozen=True)
class IntentMatch:
    intent: str
    confidence: float
    response: str


INTENT_PATTERNS: dict[str, tuple[tuple[str, ...], str]] = {
    "greeting": (
        ("hello", "hi", "hey", "good morning", "good evening"),
        "Hello! I can help with deploys, bugs, meeting notes, and status updates.",
    ),
    "deploy": (
        ("deploy", "release", "rollback", "production", "staging"),
        "Deployment checklist: run tests, confirm env vars, check migrations, "
        "verify health endpoint, and keep a rollback plan ready.",
    ),
    "bug": (
        ("bug", "error", "crash", "traceback", "issue", "broken"),
        "Please share: 1) reproduction steps, 2) expected vs actual result, "
        "3) environment, 4) recent logs or traceback.",
    ),
    "meeting": (
        ("meeting", "sync", "standup", "agenda", "notes"),
        "I can draft an agenda with: goal, blockers, decisions needed, and owners.",
    ),
    "status": (
        ("status", "progress", "update", "eta"),
        "Status template: Done / In progress / Blocked / Next. Include owners and dates.",
    ),
    "thanks": (
        ("thanks", "thank you", "thx"),
        "You're welcome. Ping me if you need a follow-up checklist.",
    ),
}


def normalize_message(text: str) -> str:
    return " ".join(text.strip().split()).lower()


def tokenize(text: str) -> set[str]:
    return set(TOKEN_RE.findall(normalize_message(text)))


def score_intent(tokens: set[str], keywords: Iterable[str]) -> float:
    hits = sum(1 for keyword in keywords if keyword in " ".join(tokens) or keyword in tokens)
    # Prefer multi-word phrase hits via substring on joined text.
    joined = " ".join(tokens)
    phrase_hits = sum(1 for keyword in keywords if " " in keyword and keyword in joined)
    total = hits + phrase_hits
    if total <= 0:
        return 0.0
    return min(1.0, total / max(2.0, len(list(keywords)) / 2.0))


def detect_intent(text: str) -> IntentMatch:
    cleaned = normalize_message(text)
    tokens = tokenize(cleaned)
    best = IntentMatch(intent="fallback", confidence=0.0, response=build_fallback(cleaned))

    for intent, (keywords, response) in INTENT_PATTERNS.items():
        hit_count = 0
        for keyword in keywords:
            if " " in keyword:
                if keyword in cleaned:
                    hit_count += 1
            elif keyword in tokens:
                hit_count += 1
        confidence = min(1.0, hit_count / 2.0) if hit_count else 0.0
        if confidence > best.confidence:
            best = IntentMatch(intent=intent, confidence=confidence, response=response)

    return best


def build_fallback(cleaned: str) -> str:
    if cleaned.endswith("?"):
        return (
            "I don't have enough context yet. Try keywords like deploy, bug, meeting, "
            "or status so I can route a useful checklist."
        )
    return (
        "Acknowledged. I can summarize tasks, deployment notes, bug triage, "
        "or meeting agendas — include one of those keywords."
    )


def build_local_response(text: str) -> str:
    """Backward-compatible helper used by CLI/tests."""
    return detect_intent(text).response


def build_rich_response(text: str, room: str | None = None) -> dict[str, str | float]:
    match = detect_intent(text)
    prefix = f"[{room}] " if room else ""
    return {
        "intent": match.intent,
        "confidence": round(match.confidence, 2),
        "response": prefix + match.response,
    }
