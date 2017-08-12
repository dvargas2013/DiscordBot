# Reaction Discord Bot
____
## Getting Started
* Have [Python 3.5](https://www.python.org/downloads/) or Greater installed
* Install [discord.py](https://github.com/Rapptz/discord.py) (Note: You don't need the voice one. But if that's the direction you're going be my guest)
* Hopefully you already have your [Discord Bot](https://discordapp.com/developers/applications/me)'s ClientID and Token ready and waiting ;P
* Create a ***constants.py*** file  
```
ClientID = "[15 digit discord id of your bot]"
 # Secret was not used but it is a character string about 32 in length
Token = "[60 character string]"
```
____
## Minor Customizations
You can create a file called ***EditPermission.ids*** with Discord IDs on seperate lines that are allowed to add and delete Reactions from the bot. It's not necessary since the non existence of the file is an indicator that anyone can edit.  
____
## Running
The .shexe files are just text files with sh/bash in them. I have my computer set up to run them on double clicks which is why they have that weird extension.  

To run interactive debug mode you need to pass in a parameter to the call. `python3 -i DzvBotMain.py 1` is enough  

If you just want to run it in the background without a terminal just run `python3 DzvBotMain.py & disown`  

That's all the .shexe files do. Look at em if you dont believe me ;P  
____
## Commands - @bot [command]
#### say/repeat - Repeats anything you type after the command

#### show/get - Show details of Emoji or Trigger
* There **should** be either an emoji or a trigger
	* If not, then replies with 10 random triggers
* Will only look at the first word after the command
* If it doesn't find a trigger, it will search for triggers that start with it
	* You can force a search by adding ellipsis anywhere in message
* Ignores capitalizations and punctuation (other than the existence of ellipsis in the message)

#### add/set - Add Emoji/Triggers to each other's list
* There **must** be at least 1 emoji at least 1 trigger
	* If not, it'll will look down on you and reply with usage help ;P
* They ***MUST*** be whitespace separated
* They can be jumbled up and in any order
* Ignores capitalizations and punctuation
* ***You must have Editing Permission to use this Command***

#### del/remove/delete - Deletes an Emoji or Trigger
* There **must** be an Emoji or Trigger
	* If not, it'll look down on you and reply with usage help ;P
* Will only look at the first word after the command
* If there are multiple Emojis or Triggers associated with the given one, will ask for confirmation
	* There is no need to @mention, a simple yes/no in the same channel will suffice
* Ignores capitalizations and punctuation
* ***You must have Editing Permission to use this Command***