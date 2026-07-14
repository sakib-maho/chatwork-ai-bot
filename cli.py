"""CLI for Chatwork AI bot local mode."""

from __future__ import annotations

import argparse
import json

from chatwork_bot.responder import build_rich_response
from chatwork_bot.service import BotService, InMemoryChatworkClient


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Local Chatwork-style AI bot")
    parser.add_argument("message", help="Incoming message text")
    parser.add_argument("--room", default="local-room")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    client = InMemoryChatworkClient()
    bot = BotService(client)
    result = bot.handle_incoming(args.room, args.message)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"intent={result['intent']} confidence={result['confidence']}")
        print(result["response"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
