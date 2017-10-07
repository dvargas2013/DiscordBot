#!/usr/bin/env python3
import discord
import asyncio

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
    Reactions.setCustoms( client.get_all_emojis() )
    if _commands.dont_react(message): return
    if "DRINK" in message.content.split() and drink.drinking_allowed(message): await drink.drink(client,message)
    # It's just a regular message nothing else to do but add a reaction
    for e in Reactions.getEmojisFromTriggersInMessage(message.content):
        await client.add_reaction(message,e)