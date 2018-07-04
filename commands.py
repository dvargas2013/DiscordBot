#!/usr/bin/env python3
import discord
import asyncio
import re
import discord.utils

# command holder
import _commands
import drink

# punctuation remover. use "[string]".translate(puncRemover)
from string import punctuation
puncRemover = str.maketrans('','',punctuation)

# Data Storage Device
Reactions = _commands.Reactions

async def command(client,message):
    splits = [i for i in message.content.lower().translate(puncRemover).split() if len(i)<15]
    # This section right here is probably the cleanest I've ever written code
    if splits[0] in ['add','set']:               await _commands.add(client,message,splits[1:])
    elif splits[0] in ['show','get']:            await _commands.show(client,message,splits[1:])
    elif splits[0] in ['remove','delete','del']: await _commands.delete(client,message,splits[1:])
    elif splits[0] in ['say','repeat']:          await _commands.repeat(client,message,splits[1:])
    # react if nothing else
    elif message.channel.is_private:             await react(client,message) 
    # anything under this cant be in private
    elif splits[0] == 'reset':                   await drink.reset(client,message)
    elif splits[0] == 'count':                   await drink.count(client,message)
    elif splits[0] == 'force':                   await drink.force(client,message)
    else:
        usage = "show/say" if _commands.cantEdit(message) else "add/show/del/say"
        await client.send_message(message.channel,'I didn\'t understand that 😦 \n Usage: "%s %s"'%(client.user.mention,usage))
async def react(client,message): # if its not a command it goes into reactions
    if _commands.dont_react(message): return
    if "DRINK" in message.content.split() and drink.drinking_allowed(message): await drink.drink(client,message)
    # It's just a regular message nothing else to do but add a reaction
    custom_emojis = list(client.get_all_emojis())
    Reactions.setCustoms( custom_emojis )
    c = 0
    for e in Reactions.getEmojisFromTriggersInMessage(message.content):
        await client.add_reaction(message,e)
        c += 1
        if c == 20: break
    # TODO make this better cause its not working unless theres a space between em
    if c == 0: # if no triggers to react to . maybe there are some emojis added to the sentence you can just copy paste
        for e in _commands.findEmojisInSplit(message.content.lower().translate(puncRemover).split()):
            await client.add_reaction(message,e)
        for e in re.findall('<:\S+:\d+>',message.content):
            E = discord.utils.get(custom_emojis, id=e[e.rfind(':')+1:-1])
            await client.add_reaction(message,E)