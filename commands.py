#!/usr/bin/env python3
import discord
import asyncio

from reactions import Reactions
Reactions = Reactions.read()

from threading import Thread
from time import sleep
def writeReactions():
    while 1:
        Reactions.write() # it has a internal dirty bit
        sleep(60) # write every minute
Thread(target = writeReactions).start()

def isEmoji(x): return len(x) == 1 and ord(x) > 255
def listify(C): return ", ".join('%r'%r for r in sorted(C))
async def add(client,message,splits):
    m = 'Usage: "%s add [emoji] [trigger]"'%client.user.mention
    if len(splits)>1:
        for i in splits: # find and remove the emoji
            if isEmoji(i):
                emoji = i
                break
        splits.remove(emoji)
        if splits:
            trigger = splits[0]
            Reactions.add(trigger,emoji)
            m = "Added %s and %s "%(emoji,trigger)
    await client.send_message(message.channel,m)
async def show(client,message,splits):
    if not splits:
        T = Reactions.triggers.keys()
        if T: m = "My triggers in here are "+listify(T)
        else: m = "I don't have triggers set"
    elif isEmoji(splits[0]):
        emoji = splits[0]
        T = Reactions.getEmoji(emoji)
        if len(T): m = repr(emoji)+" is triggered by "+listify(T)
        else:      m = repr(emoji)+" isn't triggered by anything ... yet"
    else:
        trigger = splits[0]
        E = Reactions.getTrigger(trigger)
        if len(E): m = repr(trigger)+" triggers "+listify(E)
        else:      m = repr(trigger)+" doesn't trigger anything ... yet"
    await client.send_message(message.channel,m)
async def delete(client,message,splits):
    if not splits or len(splits) > 2:
        m = 'Usage: "{0} del [emoji]" or "{0} del [trigger]"'.format(client.user.mention)
    else:
        if isEmoji(splits[0]):
            get = Reactions.getEmoji
            none = " isn't triggered by anything ..."
            rem = Reactions.removeEmoji
            sure = " triggered by "
        else:
            get = Reactions.getTrigger
            none = " doesn't trigger anything ..."
            rem = Reactions.removeTrigger
            sure = " triggers "
    
        s0 = splits[0]
        C = get(s0)
        if not C: m = repr(s0)+none
        elif len(C) == 1:
            rem(s0)
            repr(s0)+" has been removed"
        else:
            m = repr(s0)+sure+listify(C)+". Are you sure you want to remove?"
            await client.send_message(message.channel,m)
            msg = await client.wait_for_message(timeout=10,author=message.author,channel=message.channel,
            check=lambda m: 'yes' in m.clean_content.lower() or 'no' in m.clean_content.lower())
            if msg == None: m = "Looks like I'm not deleting "+repr(s0)+" any time soon"
            else:
                if 'yes' in msg.clean_content.lower():
                    rem(s0)
                    m = repr(s0)+" has been removed"
                else: m = " Deletion of "+repr(s0)+" has been canceled"
    await client.send_message(message.channel,m)

async def command(client,message):
    splits = [i for i in message.content.lower().split() if len(i)<20]
    if splits[0] in ['add','set']: await add(client,message,splits[1:])
    elif splits[0] in ['show','get']: await show(client,message,splits[1:])
    elif splits[0] in ['remove','delete','del']: await delete(client,message,splits[1:])
    else: await client.send_message(message.channel,'I didn\'t understand that 😦 \n Usage: "%s add/show/del"'%client.user.mention)
async def react(client,message):
    # It's just a regular message nothing else to do but add a reaction
    T = list(Reactions.getTriggersFromMessage(message.content))
    if not T: return
    for t in T:
        for e in Reactions.triggers.get(t,set()):
            await client.add_reaction(message,e)