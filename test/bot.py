from discord.ext.commands.errors import MissingRequiredArgument
from discord.ext.commands.help import MinimalHelpCommand
from .utils.functions import bool_switch
# from .utils.checks import is_admin
import os
import discord
from discord import Intents
from discord.ext import commands
from discord.ext.commands import is_owner
from keep_alive import keep_alive

client = commands.Bot(command_prefix = ['$', '$ '], owner_id = 287306245893914624, intents = Intents.all())
en_testing = 0

@client.event
async def on_ready():
    print(f'Bot is almost ready.')
    for guild in client.guilds:
        print(f'On {guild} (id {guild.id})')
    await client.change_presence(activity=discord.Game('currently testing'), status=discord.Status.idle)
    print(f'Bot is ready and logged in as {client.user}'.format(client))

@client.event
async def on_member_remove(member):
    print(f'{member} has left a server.')

@client.command()
async def ping(ctx):
    await ctx.send(f'{client.latency*1000}ms')

@client.command(aliases = ['mode'])
@is_owner()
async def switch_modes(ctx, en_testing):
    en_testing = not en_testing
    if en_testing: await client.change_presence(activity=discord.Game('currently testing'), status=discord.Status.idle)
    else: await client.change_presence(activity=discord.Game('yeet'), status=discord.Status.online)

# COGS
@client.command()
@is_owner()
async def load(ctx, extension):
    client.load_extension(f'test.cogs.{extension}')

@client.command()
@is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'test.cogs.{extension}')

@client.command()
@is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'test.cogs.{extension}')
    client.load_extension(f'test.cogs.{extension}')

# ERRORS
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): await ctx.send('Invalid command.')
    if isinstance(error, MissingRequiredArgument): await ctx.send('Invalid or missing argument.')

# LOAD COGS
for filename in os.listdir('./test/cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'test.cogs.{filename[:-3]}')
        print(f'Loaded {filename}')

keep_alive()
client.run(os.environ.get('TOKEN'))
