# Reaction Discord Bot
____
### Getting Started
* Have [Python 3.5](https://www.python.org/downloads/) or Greater installed
* Install [discord.py](https://github.com/Rapptz/discord.py) (Note: You don't need the voice one. But if that's the direction you're going be my guest)
* Hopefully you already have you're [Discord Bot](https://discordapp.com/developers/applications/me)'s ClientID and Token ready and waiting ;P
* Create a ***constants.py*** file  
```ClientID = "[15 digit discord id of your bot]"
 # Secret was not used but it is a character string about 32 in length
Token = "[60 character string]"```
____
### Minor Customizations
You can create a file called ***EditPermission.ids*** with Discord IDs on seperate lines that are allowed to add and delete Reactions from the bot. It's not necessary since the non existence of the file is an indicator that anyone can edit.  
____
### Running
The .shexe files are just text files with sh/bash in them. I have my computer set up to run them on double clicks which is why they have that weird extension.  

To run interactive debug mode you need to pass in a parameter to the call. `python3 -i DzvBotMain.py 1` is enough  

If you just want to run it in the background without a terminal just run `python3 DzvBotMain.py & disown`  

That's all the .shexe files do. Look at em if you dont believe me ;P  