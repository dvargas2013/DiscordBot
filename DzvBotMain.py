#!/usr/bin/env python3
import sys
DEBUG = len(sys.argv) > 1

import random
# 64 bits of randomness
CUR = random.randrange(2**(8*64)).to_bytes(64,'little')

double_stopper = "DzvBotMain.pid"

import os
def chdir():
    d = os.path.split(__file__)[0]
    if d: os.chdir(d)
chdir()
print("Current Directory Set To:",os.getcwd())
if not os.path.exists(double_stopper): 
    with open(double_stopper, "wb") as f: f.write(CUR)

import mmap
mmapfile = open(double_stopper, "r+b")
MM = mmap.mmap(mmapfile.fileno(), 0)
MM[:64] = CUR
# if the MM doesnt equal CUR anymore that means someone else started running

def checkConstants(cfile="constants.py"):
    if os.path.exists(cfile): return
    print("Go to https://discordapp.com/developers/applications/me and get the ClientID and Token")
    ClientID = input("ClientID: ")
    Token = input("Token: ")
    with open(cfile,"w") as f: f.write("ClientID = '%s'\nToken = '%s'"%(ClientID,Token))
checkConstants()

from constants import ClientID,Token

import discord
import asyncio
import commands

__doc__ = '''https://discordapp.com/oauth2/authorize?&client_id=%s&scope=bot&permissions=11328'''%ClientID

client = discord.Client()
@client.event
async def on_message(message):
    if MM[:64] != CUR:
        await client.logout()
        return

    if message.author.bot or message.author == client.user: return

    if DEBUG:
        global M
        M = message

    # If I was mentioned you want me to do something
    if (client.user.mentioned_in(message) and client.user in message.mentions) or message.channel.is_private:
        if DEBUG: print(message.clean_content)
        await commands.command(client,message)
    else: # If not mentioned I might react c;
        await commands.react(client,message)
    sys.stdout.flush()

from threading import Thread
# I dont run it directly cause I don't trust it to die on SIGTERM
t = Thread(target = lambda: client.run(Token), daemon=True)
t.start()
sys.stdout.flush()
if DEBUG:
    print(__doc__)
    from discord.utils import find # when you have a list of stuff to look through use find to find stuff for you
    RUN = client.loop.create_task # A lot of coroutines cant be run directly. Use this to run them
else:
    t.join()
    if MM[:64] == CUR: # if ended of own volition (aka error killed the thread)
        MM[:] = b"\x00"*len(MM[:])
mmapfile.close()