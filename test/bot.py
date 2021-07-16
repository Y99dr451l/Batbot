import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents(messages = True, guilds = True, reactions = True, members = True, presences = True)
client = commands.Bot(command_prefix = '$', intents = intents)

admins_file = open('admins.txt', 'r')
admins = admins_file.read().split(',')
admins_file.close()

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

# COGS
def is_admin(ctx):
    return ctx.author.id in admins

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
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid command used.')

# LOAD COGS
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')
        print(f'Loaded {filename}')

keep_alive()
client.run(os.environ.get('TOKEN'))