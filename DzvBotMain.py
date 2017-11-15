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
def listin(stringsSearch,mainString): return any((i in mainString) for i in stringsSearch)
lastLewd = None
from _commands import dont_react
async def checkForLewd(client,message):
    global lastLewd
    if dont_react(message): return
    if lastLewd == None:
        lastLewd = message.timestamp
        time = 100
    else:
        time = (message.timestamp - lastLewd).total_seconds()
    
    if time > 2 and "bot" in message.clean_content:
        lastLewd = None # u get 2 second cooldown if u say bot
        # dont update time in order to check if its <20 in sfw channels
    elif time < 10: # 10 second cooldown
        return
    stringk=message.content.lower().translate(commands.puncRemover)
    strings=[]
    active = False # if active is true it will warn in other channels. if it's false it turns off the warning
    if "nudes" in stringk:                             strings.append("Send some to me too")
    if listin(["butt","ass"],stringk):                 strings.append("( ͡° ͜ʖ ͡°) Butt?")
    if listin(["spank","choke","kink"],stringk):       strings.append("> tries to smooth out kinks\n> fails")
    if listin(["sex","bang"],stringk):                 strings.append("> MOANS")
    if listin(["suck","succ","blow"],stringk):         strings.append("SLUUUUUUURP")
    if listin(["jizz","cum","semen"],stringk):         strings.append("It's okay. I love cream on my buns too")
    if listin(["vagina","pussy"],stringk):             strings+="🐱 😺 😸 😹 😽 😻 😿 😼".split()
    if listin(["penis","dick","cock","dong"],stringk): strings.append("Are you talking about 🍆 again?")
    if strings: active = True # if one of those top ones are present you get a warning. these bottoms ones dont
    if "tit" in stringk:                       strings.append("We're talking about birds right?")
    if listin(["hot","hawt"],stringk):         strings.append("Don't worry I'll send some 🍧")
    if listin(["lewd","dirty","sin"],stringk): strings.append("> sends to the 🛁")
    if "lap" in stringk:                       strings.append("> sits")
    if listin(["gay","fag","virgin"],stringk): strings.append("I know you are but what am I?")
    if strings:
        # no matter the reason. dont spam other channels
        if message.channel.id != "238926790985252864" and time < 20: return
        
        if active and message.channel.id != "238926790985252864":
            await client.send_message(message.channel,"I see you are nsfw-ing in <#%s>. How about we all go into <#238926790985252864> c;"%message.channel.id)
        else:
            m = random.choice(strings)
            await client.send_message(message.channel,m)
        lastLewd = message.timestamp
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

    if message.server and message.server.id == '238903502125006849': await checkForLewd(client,message)
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
else: t.join()

mmapfile.close()