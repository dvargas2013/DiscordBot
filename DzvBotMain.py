#!/usr/bin/env python3
import sys
DEBUG = len(sys.argv) > 1

def pidcheckill():
    # If there is an already running Python with the pid in the pid file
    # Kill it . There can be only 1
    import os
    from subprocess import check_output
    if os.path.exists('DzvBotMain.pid'): # If it doesnt exist skip to where you make one
        pid = None # if it does exists, open it and get the pid
        with open('DzvBotMain.pid',"r") as f: pid = int(f.readline().strip())
        if pid: # if it was empty for some reason ... just skip to overwriting it
            proc = check_output("ps aux | awk -v P=%s '$2 == P { print }'"%pid,shell=True).decode()
            if proc and 'Python' in proc:
                print("Another Bot Process is already Active") # Worst case 1: Both stay running duplicating messages
                os.system("kill -TERM %s"%pid) # Worst case 2: Both are killed nothing runs
    with open('DzvBotMain.pid',"w") as f: f.write(str(os.getpid()))
pidcheckill() 

import discord
import asyncio
from commands import command, react

from constants import ClientID,Token
# Token is about 60 characters long
# Secret is about 32 characters
# ClientID is 18 characters long

__doc__ = '''https://discordapp.com/oauth2/authorize?&client_id=%s&scope=bot&permissions=0'''%ClientID

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