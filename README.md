# twitchchat-wss
Lightweight [Twitch](https://twitch.tv) chat client using 
WebSockets.

# Usage
```python
from twitchchat_wss import TwitchChatClient, Message

client = TwitchChatClient("your_name", "your_oauth_token", ["your_channel"])
client.start()
message = Message("", "your_channel", "Hey Guys HeyGuys")
client.message(message)
client.join_channel("other_channel")
for msg in client.messages():
    print(msg)
```