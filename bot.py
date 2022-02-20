import os

import discord
from discord import Intents
from discord.ext import commands
from discord.ext.commands import is_owner

from keep_alive import keep_alive

client = commands.Bot(command_prefix = '$', owner_id = 287306245893914624, intents = Intents.all())
setattr(client, 'url', 'https://github.com/Y99dr451l/Batbot')
cog_path = 'cogs.'
other_cog_path = './cogs'

@client.event
async def on_ready():
    for guild in client.guilds:
        print(f'On {guild} ({guild.id})')
    await client.change_presence(activity=discord.Game('currently testing'), status=discord.Status.idle)

@client.command()
@is_owner()
async def load(ctx, extension):
    try: client.load_extension(cog_path+f'{extension}')
    except: await ctx.send(f'Extension `{extension}` could not be loaded.'); return
    await ctx.send(f'Extension `{extension}` loaded.')

@client.command()
@is_owner()
async def unload(ctx, extension):
    try: client.unload_extension(cog_path+f'{extension}')
    except: await ctx.send(f'Extension `{extension}` could not be unloaded.'); return
    await ctx.send(f'Extension `{extension}` unloaded.')

checks = ['error', 'unloaded', 'loaded', 'reloaded']

@client.command()
@is_owner()
async def reload(ctx, extension):
    output = ''
    if extension == (None or 'all'):
        for filename in os.listdir(other_cog_path):
            if filename.endswith('.py'): output += reloadext(filename[:-3])
    else: output = reloadext(extension)
    await ctx.send(output)

def reloadext(extension):
    check = 0
    try: client.unload_extension(cog_path+f'{extension}'); check += 1
    except: pass
    try: client.load_extension(cog_path+f'{extension}'); check += 2
    except: pass
    return f'`{extension}`: {checks[check]}\n'

for filename in os.listdir(other_cog_path):
    if filename.endswith('.py'): client.load_extension(cog_path+f'{filename[:-3]}')

keep_alive()
client.run(os.environ.get('TOKEN'))
