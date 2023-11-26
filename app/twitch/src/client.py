from dataclasses import dataclass
from websocket import WebSocketApp
import threading
from queue import Queue
from typing import Iterator


@dataclass
class Credentials:
    user_name: str
    oauth_token: str


@dataclass
class Message:
    user: str
    channel: str
    text: str


class TwitchChatClient:
    def __init__(self, username: str, oauth_token: str, channels: list[str]) -> None:
        assert oauth_token.startswith("oauth:")

        self.message_queue = Queue()
        self.error_queue = Queue()
        self.connected = False
        self.lock = threading.Lock()
        self.cv_connected = threading.Condition(self.lock)
        self.closing = False
        self.credentials = Credentials(username, oauth_token)
        self.wsapp = WebSocketApp(
            "wss://irc-ws.chat.twitch.tv:443",
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close,
            on_error=self.on_error,
        )
        self.thread: threading.Thread | None = None
        self.channels = channels

    def on_open(self, wa: WebSocketApp) -> None:
        wa.send(f"PASS {self.credentials.oauth_token}")
        wa.send(f"NICK {self.credentials.user_name}")
        for channel in self.channels:
            wa.send(f"JOIN #{channel}")
        self.lock.acquire()
        self.connected = True
        self.cv_connected.notify_all()
        self.lock.release()

    def on_message(self, wa: WebSocketApp, msg: str) -> None:
        if msg.startswith("PING"):
            wa.send("PONG :tmi.twitch.tv")
        else:
            self.message_queue.put(msg)

    def on_close(
        self, wa: WebSocketApp, close_status_code: int, close_msg: str
    ) -> None:
        self.stop()

    def on_error(self, wa: WebSocketApp, error: str) -> None:
        self.error_queue.put(error)

    def messages(self) -> Iterator[str]:
        while not self.closing:
            raw_message = self.message_queue.get()
            if raw_message is None:
                break
            yield raw_message

    def errors(self) -> Iterator[str]:
        while not self.closing:
            error = self.error_queue.get()
            if error is None:
                break
            yield error

    def start(self) -> None:
        self.thread = threading.Thread(target=self.wsapp.run_forever)
        self.thread.start()

    def join_channel(self, channel_name: str) -> None:
        self.lock.acquire()
        while not self.connected:
            self.cv_connected.wait()
        self.lock.release()
        self.wsapp.send(f"JOIN #{channel_name}")

    def stop(self) -> None:
        if self.thread is not None:
            self.message_queue.put(None)
            self.error_queue.put(None)
            self.closing = True
            self.wsapp.close()
            self.thread.join()
