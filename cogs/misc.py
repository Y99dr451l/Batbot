import discord
from discord.ext import commands
from discord.ext.commands import is_owner
import requests
import json
import time
import numpy

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self} loaded.')

    rng = numpy.random.default_rng()
    starttime = time.monotonic()

    statuses = {
        'online': discord.Status.online,
        'idle': discord.Status.idle,
        'offline': discord.Status.offline,
        'dnd': discord.Status.dnd,
    }

    @commands.command()
    @is_owner()
    async def status(self, ctx, arg):
        if arg in self.statuses.keys(): await self.client.change_presence(status=self.statuses[arg])
        else: await ctx.send(f'`{arg}` is not a valid status.')

    @commands.command()
    @is_owner()
    async def activity(self, ctx):
        await self.client.change_presence(activity=discord.CustomActivity(f'{ctx.message.content[9:]}'))

    @commands.command()
    async def info(self, ctx):
        title = f'{self.client.user}'
        description = f'''
Owner: {self.client.get_user(self.client.owner_id)}
Uptime: {self.uptimecalc()}
Ping: {round(self.client.latency*1000,4)}ms
Extensions: {str(self.client.extensions.keys())[11:-2]}'''
        url = 'https://github.com/Y99dr451l/Batbot'
        embed = discord.Embed(title=title, description=description, url=url, color=self.rng.integers(0, 16777215, dtype=int))
        embed.set_footer(text=f'Information requested by: {ctx.author.display_name}')
        await ctx.send(embed=embed)
    
    def uptimecalc(self):
        if not self.starttime: self.starttime = time.monotonic()
        uptime = time.monotonic()-self.starttime
        utdys = uptime//(3600*24)
        uthrs = uptime//3600-utdys*24
        utmin = uptime//60-uthrs*60-utdys*60*24
        utsec = uptime-utmin*60-uthrs*3600-utdys*3600*24
        output = ''
        if utdys: output += f'{int(utdys)} days, '
        if uthrs: output += f'{int(uthrs)} hours, '
        if utmin: output += f'{int(utmin)} minutes, '
        return output + f'{round(utsec,4)} seconds'

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel or discord.GroupChannel):
            if message.channel.recipient.id != self.client.owner_id:
                owner = self.client.get_user(self.client.owner_id)
                await owner.send(message.author.name+' ('+str(message.author.id)+'):\n'+message.content)
    
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
        else: await ctx.send("No user set.")

def setup(client):
    client.add_cog(Misc(client))
