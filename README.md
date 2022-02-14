# Graham
A programmable bot that makes bad conversation

Graham is a chatbot whose sole purpose it to respond to certain inputs with canned phrases. Once Graham has been added to your server, any users of that server can program him via DM. He can respond to phrases with other phrases, replace phrases with other phrases, and say things at random, picked from a pool.

## How to set up Graham on Discord

Requirements:
* Python (tested on 3.6.8 or higher)
* Discord.py, tested 1.3.3
* Only tested on Linux

Clone this repo and then run graham_discord.py, providing a discord API key as the first parameter. I would recommend running him via 

```bash
nohup python3 graham_discord.py <key> &
```

## How to set up Graham on Twitch

Requirements:
* Python (tested on 3.6.8 or higher)
* twitchio.ext
* Tested on Windows & Linux

Clone this repo and then run graham_twitch.py, providing a Twitch OAuth key as the first parameter, and a comma-delimited list of channels to give graham access to. I would recommend running him via 

```bash
nohup python3 graham_discord.py <key> <channel1>,<channel2>,<channel3>... & 
```

## How to use Graham

Once Graham is running, add him to a server, giving him permission to read messages and traverse channels. Then, write a message in the server that says `~graham-help`. This will register your server with Graham, and Graham will display a help message.

## Other stuff

AGPL version 3. Send me your pull requests. `graham_discord.py` provides a discord version of graham, although you can write a Graham bot for any chat client by creating an instance of `call_response`, as defined in `call_response.py`, and sending messages to it.

## Credits

* Discord interface and permute/reply/generate/concatenate modules developed by Rob Welch
* Twitch.tv interface and rodney module developed by Brandon Sultana

Please send me your pull requests!

