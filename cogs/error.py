import discord
from discord.ext import commands

class Error(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound) and not ctx.message.content.endswith('$'): await ctx.send('Invalid command.')
        elif isinstance(error, commands.MissingRequiredArgument): await ctx.send('Invalid or missing argument.')
        elif isinstance(error, commands.MissingPermissions): await ctx.send('Missing permissions.')
        else: print(f'Ignoring exception in command {ctx.command}: {error}')

def setup(client):
    client.add_cog(Error(client))