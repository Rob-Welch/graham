# -*- coding: utf-8 -*-
"""
This is the discord fronted for call_response, otherwise known as graham.
More info at https://github.com/Rob-Welch/graham
"""

import discord
import asyncio
import call_response
import argparse

parser = argparse.ArgumentParser(description="Graham")
parser.add_argument("key", action="store", type=str, help="Discord API key")

help_msg = """Hello, I'm Graham. I like cars and car accessories. I can talk and also use memes, replacing the need for other surviving humans.

Here are my primary functions:

~graham-respond - I will respond to one phrase with another phrase. For example: ~graham-respond "come" "and also arrive" "server name"
~graham-permute - I will replace words with other words. For example: ~graham-permute "egg" "dippy egg" "server name"

You must send these commands to me in private. When you DM me, just add the name of the discord server you want them to be active on as a final parameter, e.g.

~graham-permute "gla" "graham likes automobiles" "graham's car discord"

Thank you for using Graham. Send your bug reports to the trash, I am perfect. See Graham's source code at https://github.com/Rob-Welch/graham
"""

client = discord.Client()

graham = call_response.call_response(help_msg=help_msg, decay_in=50)

@client.event
async def on_message(message):
    """
    For a given message in discord, scan that message and query a response
    from graham. If the response is not blank, send the message.
    Params:
        Message - a message object from discord.py
    Returns:
        nothin
    """
        
    if message.author == client.user:
        return
    
    server = ""
    
    if message.guild is not None:
        server = message.guild.name
    
    response = graham.parse(message.content, server)
    
    if response != "":
        await message.channel.send(response)

if __name__ == "__main__":
    args = parser.parse_args()
    client.run(args.key)