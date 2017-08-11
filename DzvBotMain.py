#!/usr/bin/env python3
import discord
import asyncio
from commands import command, react

from constants import ClientID,Token
# Token is about 60 characters long
# Secret is about 32 characters
# ClientID is 18 characters long

__doc__ = '''https://discordapp.com/oauth2/authorize?&client_id=%s&scope=bot&permissions=0'''%ClientID

import sys
DEBUG = len(sys.argv) > 1

client = discord.Client()
@client.event
async def on_message(message):
    if message.author.bot or message.author == client.user: return
    
    if DEBUG:
        global M
        M = message

    # If I was mentioned you want me to do something
    if client.user.mentioned_in(message):
        if DEBUG: print(message.clean_content)
        await command(client,message)
    else: # If not mentioned I might react c;
        await react(client,message)

if DEBUG:
    print(__doc__)
    from discord.utils import find # when you have a list of stuff to look through use find to find stuff for you
    # dont block the interactive
    from threading import Thread
    Thread(target = lambda: client.run(Token)).start()
    RUN = client.loop.create_task # A lot of coroutines cant be run directly. Use this to run them
else:
    # this is a blocking call
    client.run(Token)