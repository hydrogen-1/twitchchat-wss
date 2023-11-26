# twitchchat-wss
Lightweight [Twitch](https://twitch.tv) chat client using 
WebSockets.

# Usage
```python
from twitchchat_wss import TwitchChatClient

client = TwitchChatClient("your_name", "your_oauth_token", ["your_channel"])
client.start()
for msg in client.messages():
    print(msg)
```