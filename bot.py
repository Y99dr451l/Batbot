from discord.ext.commands.errors import MissingPermissions, MissingRequiredArgument
# from discord.ext.commands.help import MinimalHelpCommand
import os
import discord
from discord import Intents
from discord.ext import commands
from discord.ext.commands import is_owner
from keep_alive import keep_alive

client = commands.Bot(command_prefix = ['$', '$ '], owner_id = 287306245893914624, intents = Intents.all())
cog_path = 'cogs.'
other_cog_path = './cogs'

@client.event
async def on_ready():
    print(f'Bot is almost ready.')
    for guild in client.guilds:
        print(f'On {guild} (id {guild.id})')
    await client.change_presence(activity=discord.Game('currently testing'), status=discord.Status.idle)
    print(f'Bot is ready and logged in as {client.user}'.format(client))

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

# ERRORS
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound) and not ctx.message.content.endswith('$'): await ctx.send('Invalid command.')
    elif isinstance(error, MissingRequiredArgument): await ctx.send('Invalid or missing argument.')
    elif isinstance(error, MissingPermissions): await ctx.send('Missing permissions.')

loadall()
keep_alive()
client.run(os.environ.get('TOKEN'))