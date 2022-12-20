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
parser.add_argument("apikey", action="store", type=str, help="Discord API key")
parser.add_argument("cryptokey", action="store", type=str, help="Encryption key")
args = parser.parse_args()

with open ("graham_help.txt", "r") as file:
    help_msg = file.readlines()

client = discord.Client()

graham = call_response.call_response(help_msg=help_msg, decay_in=50, cryptokey=args.cryptokey)

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
    
    response = graham.parse(message.content, server, username=message.author.id)
    
    if response != "":
        await message.channel.send(response)

if __name__ == "__main__":
    client.run(args.key)