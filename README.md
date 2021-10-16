# Batbot
A simple and relatively useless bot for my section server on Discord using the discord.py library.

It's essentially a coding project with no real purpose yet, but I'll try to keep adding functions.
It uses a pretty bare-bones Flask implementation for the websocket which I found in a long lost tutorial.
The main.py is the earliest attempt at making the bot and has finally been rewritten using some semblance of an understanding of the Discord library in the test folder.
the first version was based off a very basic tutorial, then I started coding the prettier and modular version guided by Lucas' amazing "Discord.py Rewrite" series on YouTube.
I now use wild googling and sometimes even the library's documentation to add further things.

Some other functions I might add in the future are a gif renderer backed by a game-of-life style algorithm, some voice-chat actions, statistics for the mini-games and maybe something with Discord's new button components.

Also, a bunch of early commits were only used to push and debug the code on my EC2 server and thus don't all work properly.
I have now gotten my WSL configured and can finally debug the versions there, since I stay away from Windows for executing code after truly horrible experiences in the past.

## How to run
To run the bot, just launch main.py with Python 3. The necessary packages are discord.py, flask, numpy, sympy and possibly some other ones.
You will need to save the bot's token from the Discord Developer Portal as an environment variable named TOKEN.
You will also want to change the owner's ID of the bot to yours in order to have the permission to use all the bot's commands.
I might export these IDs to a separate file to make configuration more practical.
