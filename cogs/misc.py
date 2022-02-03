import discord
from discord.ext import commands
from discord.ext.commands import is_owner
import requests
import json

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self} loaded.')

    last_channel:str = None

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left a server.')

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel or discord.GroupChannel):
            if message.channel.recipient.id != self.client.owner_id:
                owner = self.client.get_user(self.client.owner_id)
                await owner.send(message.author.name+' ('+str(message.author.id)+'):\n'+message.content)

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
    
    @commands.command()
    @is_owner()
    async def send(self, ctx):
        message = ctx.message.content[6:]
        if len(message) > 18:
            channel_id = message[-18:]
            if channel_id.isdecimal():
                self.last_channel = int(channel_id)
                message = message[:-18]
        if self.last_channel:
            channel = self.client.get_channel(self.last_channel)
            await channel.send(message)
        else: await ctx.send("No channel set.")

    @commands.command()
    @is_owner()
    async def dm(self, ctx):
        message = ctx.message.content[4:]
        if len(message) > 18:
            user_id = message[-18:]
            if user_id.isdecimal():
                self.last_user = int(user_id)
                message = message[:-18]
        if self.last_user:
            user = self.client.get_user(self.last_user)
            await user.send(message)
        else: await ctx.send("No channel set.")

def setup(client):
    client.add_cog(Misc(client))
