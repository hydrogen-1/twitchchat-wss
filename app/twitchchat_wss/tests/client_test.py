import unittest
from unittest.mock import MagicMock, call
from app.twitchchat_wss import TwitchChatClient, Message


class TestTwitchChatClient(unittest.TestCase):
    def setUp(self):
        self.mock_wsapp = MagicMock()
        self.twitch_client = TwitchChatClient(
            "mock_username",
            "oauth:mock_oauth_token",
            ["mock_channel", "mock_channel_1"],
        )
        self.twitch_client.wsapp = self.mock_wsapp

    def test_connect(self):
        self.twitch_client.on_open(self.mock_wsapp)
        expected_calls = [
            call("PASS oauth:mock_oauth_token"),
            call("NICK mock_username"),
            call("JOIN #mock_channel"),
            call("JOIN #mock_channel_1"),
        ]
        self.mock_wsapp.send.assert_has_calls(expected_calls)
        self.assertTrue(self.twitch_client.connected)

    def test_join(self):
        self.twitch_client.on_open(self.mock_wsapp)
        self.twitch_client.join_channel("new_channel")
        expected_calls = [
            call("PASS oauth:mock_oauth_token"),
            call("NICK mock_username"),
            call("JOIN #mock_channel"),
            call("JOIN #mock_channel_1"),
            call("JOIN #new_channel"),
        ]
        self.mock_wsapp.send.assert_has_calls(expected_calls)
        self.assertTrue(self.twitch_client.connected)

    def test_message(self):
        self.twitch_client.on_open(self.mock_wsapp)
        self.twitch_client.on_message(self.mock_wsapp, "This is a test")
        messages = self.twitch_client.messages()
        self.assertIn("This is a test", messages)
        self.assertTrue(self.twitch_client.connected)

    def test_ping(self):
        self.twitch_client.on_open(self.mock_wsapp)
        self.twitch_client.on_message(self.mock_wsapp, "PING :tmi.twitch.tv")
        expected_calls = [
            call("PASS oauth:mock_oauth_token"),
            call("NICK mock_username"),
            call("JOIN #mock_channel"),
            call("JOIN #mock_channel_1"),
            call("PONG :tmi.twitch.tv"),
        ]
        self.mock_wsapp.send.assert_has_calls(expected_calls)
        self.assertTrue(self.twitch_client.connected)

    def test_send(self):
        self.twitch_client.on_open(self.mock_wsapp)
        message = Message("testUser", "testChannel", "test")
        self.twitch_client.send_message(message)
        expected_calls = [
            call("PASS oauth:mock_oauth_token"),
            call("NICK mock_username"),
            call("JOIN #mock_channel"),
            call("JOIN #mock_channel_1"),
            call(f"PRIVMSG #{message.channel} :{message.text}"),
        ]
        self.mock_wsapp.send.assert_has_calls(expected_calls)
        self.assertTrue(self.twitch_client.connected)


if __name__ == "__main__":
    unittest.main()
