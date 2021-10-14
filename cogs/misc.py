import discord
from discord.ext import commands
#from discord.ext.commands import is_owner
import requests
import json

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self} loaded.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left a server.')

    @commands.command(aliases = ['lat', 'ping'])
    async def latency(self, ctx):
        await ctx.send(f'{round(self.client.latency*1000,4)}ms')
    
    @commands.command(aliases = ['q'])
    async def quote(self, ctx, apiname = None):
        if apiname == None: await ctx.send('The possible arguments currently are `zen` and `kanye`.')
        elif apiname == 'zen':
            response = requests.get("https://zenquotes.io/api/random")
            json_data = json.loads(response.text)
            await ctx.send(json_data[0]["q"]+'\n- '+json_data[0]["a"])
        elif apiname == 'kanye':
            response = requests.get("https://api.kanye.rest")
            json_data = json.loads(response.text)
            await ctx.send(json_data["quote"]+'\n- Kanye West')

def setup(client):
    client.add_cog(Misc(client))
