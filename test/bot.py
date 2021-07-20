import os

from discord.ext.commands.errors import MissingRequiredArgument
from test.utils.functions import bool_switch
from test.utils.checks import is_admin
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '$', intents = intents)
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
@commands.check(is_admin)
async def switch_modes(ctx, en_testing):
    en_testing = bool_switch(en_testing)
    if en_testing == 1: await client.change_presence(activity=discord.Game('currently testing'), status=discord.Status.idle)
    else: await client.change_presence(activity=discord.Game('yeet'), status=discord.Status.online)

# COGS
@client.command()
@commands.check(is_admin)
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

@client.command()
@commands.check(is_admin)
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

@client.command()
@commands.check(is_admin)
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')

# ERRORS
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound): await ctx.send('Invalid command.')
    if isinstance(error, MissingRequiredArgument): await ctx.send('Invalid or missing argument.')

# LOAD COGS
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename}')

keep_alive()
client.run(os.environ.get('TOKEN'))
