from discord.ext.commands.errors import MissingPermissions, MissingRequiredArgument
# from discord.ext.commands.help import MinimalHelpCommand
import os
import discord
import time
from discord import Intents
from discord.ext import commands
from discord.ext.commands import is_owner
from keep_alive import keep_alive

client = commands.Bot(command_prefix = ['$', '$ '], owner_id = 287306245893914624, intents = Intents.all())
cog_path = 'test.cogs.'
other_cog_path = './test/cogs'
en_testing = 0
starttime = time.monotonic()

@client.event
async def on_ready():
    print(f'Bot is almost ready.')
    for guild in client.guilds:
        print(f'On {guild} (id {guild.id})')
    await switch_status()
    print(f'Bot is ready and logged in as {client.user}'.format(client))

# GENERAL
@client.command(aliases = ['up', 'ut', 'alive'])
async def uptime(ctx):
    uptime = time.monotonic()-starttime
    utdys = uptime/(3600*24)
    uthrs = uptime/3600-utdys*24
    utmin = uptime/60-uthrs*60-utdys*60*24
    utsec = uptime-utmin*60-uthrs*3600-utdys*3600*24
    output = 'The bot has been up for '
    if utdys: output += f'{utdys} days, '
    if uthrs: output += f'{uthrs} hours, '
    if utmin: output += f'{utmin} minutes, '
    await ctx.send(output + f'{utsec} seconds.')

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

@client.command(aliases = ['lat'])
async def latency(ctx):
    await ctx.send(f'{round(client.latency*1000,4)}ms')

@client.command()
@is_owner()
async def mode(ctx):
    await switch_status()

async def switch_status():
    global en_testing
    en_testing = not en_testing
    if en_testing: await client.change_presence(activity=discord.Game('currently testing'), status=discord.Status.idle)
    else: await client.change_presence(activity=discord.Game('yeet'), status=discord.Status.online)

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

# ERRORS
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): await ctx.send('Invalid command.')
    elif isinstance(error, MissingRequiredArgument): await ctx.send('Invalid or missing argument.')
    elif isinstance(error, MissingPermissions): await ctx.send('Missing permissions.')

# LOAD COGS
for filename in os.listdir(other_cog_path):
    if filename.endswith('.py'):
        client.load_extension(cog_path+f'{filename[:-3]}')
        print(f'Loaded {filename}')

keep_alive()
client.run(os.environ.get('TOKEN'))