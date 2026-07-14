# Chatwork AI Bot

Local-first Chatwork-style bot framework with intent routing, a mock API client, CLI, and tests.

## Features

- Intent detection: greeting, deploy, bug, meeting, status, thanks
- Confidence-scored routing with fallback guidance
- `BotService` + in-memory Chatwork client for offline demos/tests
- CLI for quick local replies
- Unit tests for intents and outbound messaging

## Quick start

```bash
PYTHONPATH=. python3 cli.py "Need help with production deploy"
PYTHONPATH=. python3 cli.py "We hit a bug in login" --json
PYTHONPATH=. python3 -m unittest discover -s tests -p "test_*.py"
```

## Example

```bash
$ PYTHONPATH=. python3 cli.py "hello"
intent=greeting confidence=0.5
[local-room] Hello! I can help with deploys, bugs, meeting notes, and status updates.
```

## License

MIT
