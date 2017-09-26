# TODO make the DRINKS in the data
DRINKS = dict() # dict( server -> dict( user -> int ) )

from _commands import read
DrinkPerms = read("DrinkingAllowed.ids")
def drinking_allowed(message): return message.channel.id in DrinkPerms

async def reset(client,message):
    if not message.channel.permissions_for(message.author).manage_messages:
        s = "You need 'Edit Messages' permissions in order to reset the drinks counter"
    else:
        users = root_drinkNonZero(message.server)
        if len(users) == 0: s = "No one ... has ... drunk anything ... yet"
        else:
            s = string_drinkGet(message.server,users) + "\nBut now everyone has drunk none...don't ask how"
            root_drinkNone(message.server,users)
    await client.send_message(message.channel,s)
async def count(client,message):
    users = [i for i in message.mentions if i != client.user]

    if message.channel.permissions_for(message.author).manage_messages: # do anything
        if len(users) == 0: users = root_drinkNonZero(message.server)
        
        if len(users) == 0: s = "No one has drunk anything yet"
        else: s = string_drinkGet(message.server,users)
    else: # only allowed to get 1 at a time
        if len(u) == 1: s = string_drinkGet(message.server,users)
        else: s = "You need 'Edit Messages' permissions in order to show multiple people's drink"
    
    await client.send_message(message.channel,s)
async def force(client,message):
    if not message.channel.permissions_for(message.author).manage_messages:
        await client.send_message(message.channel,"You need 'Edit Messages' permissions in order to force someone to drink")
        return
    users = [i for i in message.mentions if i != client.user]
    if len(users) == 0: s = "You need to ... you know ... tag someone"
    else: s = string_drinkIncr(message.server,users)
    await client.send_message(message.channel,s)
async def drink(client,message): await client.send_message(message.channel, string_drinkIncr(message.server,[message.author]))

def string_drinkString(name,n): return "%s has had %s drink%s"%(name,n,'' if n==1 else 's')
def string_drinkGet(server,users): return "```\n%s```"%( '\n'.join(string_drinkString(u.display_name,n) for u,n in zip(users,root_drinkGet(server,users))) )
def string_drinkIncr(server,users):
    root_drinkIncr(server,users)
    return string_drinkGet(server,users)

def root_drinkIncr(server,users):
    ds = DRINKS[server] = DRINKS.get(server,dict())
    for user in users: ds[user] = ds.get(user,0) + 1
def root_drinkGet(server,users):
    ds = DRINKS[server] = DRINKS.get(server,dict())
    return [ds.get(user,0) for user in users]
def root_drinkNone(server,users): DRINKS[server] = dict()
def root_drinkNonZero(server):
    ds = DRINKS[server] = DRINKS.get(server,dict())
    return list(ds.keys())