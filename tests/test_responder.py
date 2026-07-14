import unittest

from chatwork_bot.responder import build_local_response, detect_intent
from chatwork_bot.service import BotService, InMemoryChatworkClient


class ResponderTests(unittest.TestCase):
    def test_normalize_and_deploy_intent(self):
        match = detect_intent("Need help with production deploy")
        self.assertEqual(match.intent, "deploy")
        self.assertIn("checklist", match.response.lower())

    def test_bug_intent(self):
        response = build_local_response("We found a bug in checkout")
        self.assertIn("reproduction", response.lower())

    def test_fallback_question(self):
        match = detect_intent("What do you think?")
        self.assertEqual(match.intent, "fallback")

    def test_bot_service_sends_message(self):
        client = InMemoryChatworkClient()
        bot = BotService(client)
        result = bot.handle_incoming("room-1", "hello there")
        self.assertEqual(result["intent"], "greeting")
        self.assertEqual(len(client.sent), 1)
        self.assertEqual(client.sent[0]["room_id"], "room-1")


if __name__ == "__main__":
    unittest.main()
