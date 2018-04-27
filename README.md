# Reaction Discord Bot
____
## Getting Started
* Have [Python 3.5](https://www.python.org/downloads/) or Greater installed
* Install [discord.py](https://github.com/Rapptz/discord.py) (Note: You don't need the voice one. But if that's the direction you're going be my guest)
* Hopefully you already have your [Discord Bot](https://discordapp.com/developers/applications/me)'s ClientID and Token ready and waiting ;P
* When you first run it it will ask for a ClientID and Token. These things will save in a ***constants.py*** file
```
ClientID = "[15 digit discord id of your bot]"
Token = "[60 character string]"
```
____
## Minor Customizations
* You can create a file called ***EditPermission.ids*** with Discord IDs on separate lines that are allowed to add and delete Reactions from the bot. It's not necessary since the non existence of the file is an indicator that anyone can edit.  
* You can create a file called ***DontReactChats.ids*** with Channel IDs where you don't want the bot to attach reactions to.
* You can create a file called ***DrinkingAllowed.ids*** with Channel IDs where saying the word "DRINK" makes the author of the message increment a drink counter.
* You may use my [reactions.data](https://www.dropbox.com/s/9g25ke0g90sh32s/reactions.data?dl=0) or you may start your own. It's your choice. Using the bot commands to add and remove isn't that difficult to populate the bot with enough reactions to be cool.
____
## Running
The .shexe files are just text files with sh/bash in them. I have my computer set up to run them on double clicks which is why they have that weird extension.  

To run interactive debug mode you need to pass in a parameter to the call. `python3 -i DzvBotMain.py 1` is enough  

If you just want to run it in the background without a terminal just run `python3 DzvBotMain.py & disown`  

***Debug.shexe*** does the interactive debug mode exactly as explained but ***Main.shexe*** is a bit more advanced in that: it figures out if it was interrupted (either by sigterm or by another instance of the bot) or not. If the bot ends with no errors, ***Main.shexe*** will start another Instance  
____
## Commands - @bot [command]
### Globals
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
* ***You must have Editing Permission (Set in EditPermissions.ids) to use this Command***

#### del/remove/delete - Deletes an Emoji or Trigger
* There **must** be an Emoji or Trigger
	* If not, it'll look down on you and reply with usage help ;P
* Will only look at the first word after the command
* If there are multiple Emojis or Triggers associated with the given one, will ask for confirmation
	* There is no need to @mention, a simple yes/no in the same channel will suffice
* Ignores capitalizations and punctuation
* ***You must have Editing Permission (Set in EditPermissions.ids) to use this Command***

### Channel Specific
#### reset - Reset the Drinking counters back to zero
* Will only look at the first word not including the @mention
* Ignores capitalizations and punctuation
* ***Can only be used if you have manages_messages permissions in that channel***
#### count - Show anyone's or everyone's counters
* Will only look at the first word not including the @mention
* Ignores capitalizations and punctuation
* Can be used by anyone if you @mention who you want to see
* @mention no one to show anyone that has drank before
* ***You may list multiple people but that can only be used if you have manages_messages permissions in that channel***
#### force - Force someone to drink
* Will only look at the first word not including the @mention
* Ignores capitalizations and punctuation
* ***Can only be used if you have manages_messages permissions in that channel***