#!/usr/bin/env python3
import discord
import asyncio
from random import sample

from reactions import Reactions
Reactions = Reactions.read()

from string import punctuation
puncRemover = str.maketrans('','',punctuation)

from threading import Thread
from time import sleep
def writeReactions():
    while 1:
        Reactions.write() # it has a internal dirty bit
        sleep(60) # write every minute
Thread(target = writeReactions).start()

from os.path import exists
def read(f="EditPermission.ids"):
    if not exists(f): yield '174867952699441152'
    else:
        with open(f,'r') as fi:
            yield from fi.readlines()

EditPerms = set(i.strip() for i in read())

def isEmoji(x): return all(ord(x) > 255 for x in x)
def listify(C): return ", ".join('%s'%r for r in sorted(C))
async def add(client,message,splits):
    m = 'Usage: "%s add [emoji] [trigger]"'%client.user.mention
    if message.author.id not in EditPerms:
        m = "You dont have permission to Edit Entries"
    elif len(splits)>1:
        emoji = ""
        emojis = [i for i in splits if isEmoji(i)] # find and remove the emoji
        for e in emojis: splits.remove(e)
        triggers = splits
        
        for e in emojis:
            for t in triggers:
                Reactions.add(t,e)
        m = "Added %s and %s"%(listify(emojis),listify(triggers))
    await client.send_message(message.channel,m)
async def show(client,message,splits):
    if not splits:
        T = Reactions.triggers.keys()
        if T: m = "Here are 10 random triggers I have "+listify(sample(list(T),10))
        else: m = "I don't have triggers set"
    elif isEmoji(splits[0]):
        emoji = splits[0]
        T = Reactions.getEmoji(emoji)
        if len(T): m = '%s is triggered by %s'%(emoji,listify(T))
        else:      m = '%s isn\'t triggered by anything ... yet'%emoji
    else:
        trigger = splits[0]
        E = Reactions.getTrigger(trigger)
        if len(E): m = '%s triggers %s'%(trigger,listify(E))
        else:
            T = [t for t in Reactions.triggers.keys() if t.startswith(trigger.lower())]
            if len(T) == 1: m = '"%s" is the only trigger that starts with %s'%(T[0],trigger)
            elif T: m = '%s are all triggers that start with "%s..."'%(listify(T),trigger)
            else: m = '"%s" doesn\'t trigger anything ... yet'%trigger
    await client.send_message(message.channel,m)
async def delete(client,message,splits):
    if message.author.id not in EditPerms:
        m = "You dont have permission to Edit Entries"
    elif not splits or len(splits) > 2:
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
        if not C: m = ('"%s"'%s0)+none
        elif len(C) == 1:
            rem(s0)
            m = '"%s" has been removed'%(s0)
        else:
            m = '"%s"%s%s. Are you sure you want to remove?'%(s0,sure,listify(C))
            await client.send_message(message.channel,m)
            msg = await client.wait_for_message(timeout=10,author=message.author,channel=message.channel,
            check=lambda m: 'yes' in m.clean_content.lower() or 'no' in m.clean_content.lower())
            if msg == None: m = 'Looks like I\'m not deleting "%s" any time soon'%s0
            elif 'yes' in msg.clean_content.lower():
                rem(s0)
                m = '"%s" has been removed'%s0
            else: m = 'Deletion of "%s" has been canceled'%s0
    await client.send_message(message.channel,m)
async def repeat(client,message,splits):
    m = message.content[message.content.find(" ",message.content.find(" ")+1)+1:]
    await client.send_message(message.channel,m)
    await client.delete_message(message)
async def command(client,message):
    splits = [i for i in message.content.lower().translate(puncRemover).split() if len(i)<15]
    if splits[0] in ['add','set']: await add(client,message,splits[1:])
    elif splits[0] in ['show','get']: await show(client,message,splits[1:])
    elif splits[0] in ['remove','delete','del']: await delete(client,message,splits[1:])
    elif splits[0] in ['say','repeat']: await repeat(client,message,splits[1:])
    else: await client.send_message(message.channel,'I didn\'t understand that 😦 \n Usage: "%s add/show/del/say"'%client.user.mention)
async def react(client,message):
    # It's just a regular message nothing else to do but add a reaction
    T = list(Reactions.getTriggersFromMessage(message.content))
    if not T: return
    for t in T:
        for e in Reactions.triggers.get(t,set()):
            await client.add_reaction(message,e)