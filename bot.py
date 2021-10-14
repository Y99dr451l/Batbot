# from discord.ext.commands.help import MinimalHelpCommand
import os
import discord
import time
from discord import Intents
from discord.ext import commands
from discord.ext.commands import is_owner
from discord.ext.commands.errors import (MissingPermissions, MissingRequiredArgument)
from keep_alive import keep_alive

client = commands.Bot(command_prefix = ['$', '$ '], owner_id = 287306245893914624, intents = Intents.all())
cog_path = 'cogs.'
other_cog_path = './cogs'
en_testing = True
starttime = 0

@client.event
async def on_ready():
    print(f'Bot is almost ready.')
    for guild in client.guilds:
        print(f'On {guild} (id {guild.id})')
    await client.change_presence(activity=discord.Game('currently testing'), status=discord.Status.idle)
    print(f'Bot is ready and logged in as {client.user}'.format(client))
    global starttime
    starttime = time.monotonic()

# COGS
@client.command()
@is_owner()
async def load(ctx, extension):
    client.load_extension(cog_path+f'{extension}')

@client.command()
@is_owner()
async def unload(ctx, extension):
    client.unload_extension(cog_path+f'{extension}')

@client.command()
@is_owner()
async def reload(ctx, extension):
    client.unload_extension(cog_path+f'{extension}')
    client.load_extension(cog_path+f'{extension}')

@client.command()
@is_owner()
async def loadall(ctx):
    for filename in os.listdir(other_cog_path):
        if filename.endswith('.py'): client.load_extension(cog_path+f'{filename[:-3]}')

@client.command(aliases = ['up', 'ut'])
async def uptime(ctx):
    global starttime
    if not starttime:
        starttime = time.monotonic()
        await ctx.send('starttime has been set now.')
    uptime = time.monotonic()-starttime
    utdys = uptime//(3600*24)
    uthrs = uptime//3600-utdys*24
    utmin = uptime//60-uthrs*60-utdys*60*24
    utsec = uptime-utmin*60-uthrs*3600-utdys*3600*24
    output = 'The bot has been up for '
    if utdys: output += f'{int(utdys)} days, '
    if uthrs: output += f'{int(uthrs)} hours, '
    if utmin: output += f'{int(utmin)} minutes, '
    await ctx.send(output + f'{round(utsec,4)} seconds.')

# ERRORS
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) and not ctx.message.content.endswith('$'): await ctx.send('Invalid command.')
    elif isinstance(error, MissingRequiredArgument): await ctx.send('Invalid or missing argument.')
    elif isinstance(error, MissingPermissions): await ctx.send('Missing permissions.')

@client.command()
@is_owner()
async def mode(ctx):
    global en_testing
    en_testing = not en_testing
    if en_testing:
        await client.change_presence(activity=discord.Game('currently testing'), status=discord.Status.idle)
        await ctx.send('Changed status to **idle (testing)**.')
    else:
        await client.change_presence(activity=discord.Game('yeet'), status=discord.Status.online)
        await ctx.send('Changed status to **online**.')

for filename in os.listdir(other_cog_path):
    if filename.endswith('.py'): client.load_extension(cog_path+f'{filename[:-3]}')

keep_alive()
client.run(os.environ.get('TOKEN'))
