#!/usr/bin/env python3
import discord
import asyncio
from commands import command, react
'''
https://discordapp.com/oauth2/authorize?&client_id=219643598839218176&scope=bot&permissions=0
'''

client = discord.Client()
@client.event
async def on_message(message):
    if message.author.bot or message.author == client.user: return
    
    global M
    M = message
    
    # Emoji/Trigger Holder
    if message.server:
        # If I was mentioned you want me to do something
        if client.user.mentioned_in(message):
    #        print(message.clean_content)
            await command(client,message)
        else: # If not mentioned I might react c;
            await react(client,message)

from constants import Token
# Token is about 60 characters long
# Secret is about 32 characters
# ClientID is 18 characters long

from discord.utils import find
from threading import Thread
Thread(target = lambda: client.run(Token)).start()
RUN = client.loop.create_task
from done.String import showInfo

#client.run(Token)