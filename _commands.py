from reactions import Reactions
Reactions = Reactions.read()

# List of People's IDs that can edit the bot
from os.path import exists
def read(f):
    if exists(f):
        with open(f,'r') as fi:
            yield from fi.readlines()
EditPerms = set(i.strip() for i in read("EditPermission.ids"))
ReactPerms = set(i.strip() for i in read("DontReactChats.ids"))

def cantEdit(message):
    # If EditPerms doesnt exist anyone can edit
    # If it does exist and you're not in there ... You cant edit
    return bool(EditPerms) and message.author.id not in EditPerms
def isEmoji(x): return all(ord(x) > 255 for x in x)
def listify(C): return ", ".join('%s'%r for r in sorted(C))
def dont_react(message): return message.channel.id in ReactPerms


async def add(client,message,splits):
    m = 'Usage: "%s add [emoji] [trigger]"'%client.user.mention
    if cantEdit(message):
        m = "You dont have permission to Edit Entries"
    elif len(splits)>1:
        emoji = ""
        emojis = [i for i in splits if isEmoji(i)] # find and remove the emoji
        for e in emojis: splits.remove(e)
        triggers = splits
        if emojis and triggers:
            for e in emojis:
                for t in triggers:
                    Reactions.add(t,e)
            m = "Added %s and %s"%(listify(emojis),listify(triggers))
            print(m)
            Reactions.write()
    await client.send_message(message.channel,m)

from random import sample # Used when returning 10 random triggers
async def show(client,message,splits):
    if not splits:
        T = Reactions.getTriggers()
        if T: m = "Here are 10 random triggers I have "+listify(sample(list(T),10))
        else: m = "I don't have triggers set"
    elif isEmoji(splits[0]):
        emoji = splits[0]
        T = Reactions.getTriggersFromEmoji(emoji)
        if len(T): m = '%s: %s'%(emoji,listify(T))
        else:      m = '%s isn\'t triggered by anything ... yet'%emoji
    else:
        trigger = splits[0]
        E = []
        m = False
        if "..." not in message.clean_content:
            E = Reactions.getEmojisFromTrigger(trigger)
            if len(E): m = '%s: %s'%(trigger,listify(str(e) for e in E))
        else:
            T = [t for t in Reactions.getTriggers() if t.startswith(trigger.lower())]
            if len(T) == 1: m = '"%s" is the only trigger that starts with "%s..."'%(T[0],trigger)
            elif T: m = '%s are all triggers that start with "%s..."'%(listify(T),trigger)
        if not m: m = '"%s" doesn\'t trigger anything ... yet'%trigger
    await client.send_message(message.channel,m)


async def delete(client,message,splits):
    if cantEdit(message):
        m = "You dont have permission to Edit Entries"
    elif not splits or len(splits) > 2:
        m = 'Usage: "{0} del [emoji]" or "{0} del [trigger]"'.format(client.user.mention)
    else:
        # Both were almost exactly the same so to reduce code repetition I did this
        if isEmoji(splits[0]):
            get = Reactions.getTriggersFromEmoji
            none = " isn't triggered by anything ..."
            rem = Reactions.removeEmoji
            sure = " triggered by "
        else:
            get = Reactions.getEmojisFromTrigger
            none = " doesn't trigger anything ..."
            rem = Reactions.removeTrigger
            sure = " triggers "
        # This is the part where it was repeated
        s0 = splits[0] # imagine s0 is either emoji or trigger
        C = get(s0) # C is T or E (Aka a capital letter)
        if not C: m = ('"%s"'%s0)+none
        elif len(C) == 1:
            rem(s0) # rem is defined above
            m = '"%s" has been removed'%(s0)
            print(m)
            Reactions.write()
        else:
            m = '"%s"%s%s. Are you sure you want to remove?'%(s0,sure,listify(C))
            await client.send_message(message.channel,m)
            msg = await client.wait_for_message(timeout=10,author=message.author,channel=message.channel,
            check=lambda m: 'yes' in m.clean_content.lower() or 'no' in m.clean_content.lower())
            if msg == None: m = 'Looks like I\'m not deleting "%s" any time soon'%s0
            elif 'yes' in msg.clean_content.lower():
                rem(s0) # rem is defined above
                m = '"%s" has been removed'%s0
                print(m)
                Reactions.write()
            else: m = 'Deletion of "%s" has been canceled'%s0
    await client.send_message(message.channel,m)


async def repeat(client,message,splits):
    m = message.content
    m = m[m.lower().find(splits[0]):]
    await client.send_message(message.channel,m) # Repeat
    if not message.channel.is_private and message.server.get_member(client.user.id).permissions_in(message.channel).manage_messages:
        await client.delete_message(message) # And Delete Original Message (No one must know)