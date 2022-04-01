import json
import time

import discord
import numpy
import requests
from discord.ext import commands
from discord.ext.commands import is_owner

output = ''

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.cstatus = discord.Status.online
        self.cactivity = ''
        self.rng = numpy.random.default_rng()
        self.starttime = self.client.starttime

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self} loaded.')

    statuses = {
        'online': discord.Status.online,
        'idle': discord.Status.idle,
        'offline': discord.Status.offline,
        'dnd': discord.Status.dnd,
    }

    @commands.command()
    @is_owner()
    async def status(self, ctx, arg):
        if arg in self.statuses.keys():
            self.cstatus = self.statuses[arg]
            await self.client.change_presence(activity=discord.Game(name=self.cactivity), status=self.cstatus)
        else: await ctx.send(f'`{arg}` is not a valid status.')

    @commands.command()
    @is_owner()
    async def activity(self, ctx):
        content = ctx.message.content
        if len(content) > 10: self.cactivity = content[10:]
        await self.client.change_presence(activity=discord.Game(name=self.cactivity), status=self.cstatus)

    @commands.command()
    async def info(self, ctx):
        title = f'{self.client.user}'
        url = self.client.url
        color = self.rng.integers(0, 255, dtype=int) + self.rng.integers(0, 255, dtype=int)*256 + self.rng.integers(0, 255, dtype=int)*256*256
        embed = discord.Embed(title=title, url=url, color=color)
        embed.add_field(name='Owner', value=f'{self.client.get_user(self.client.owner_id)}')
        embed.add_field(name='Uptime', value=f'{self.uptimecalc()}')
        embed.add_field(name='Latency', value=f'{round(self.client.latency*1000,4)}ms')
        embed.add_field(name='Extensions', value=f'{str(self.client.extensions.keys())[11:-2]}', inline=False)
        embed.set_footer(text=f'Information requested by: {ctx.author.display_name}\nColour: {hex(color)}')
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
    async def exec(self, ctx):
        message = ctx.message.content[6:]
        try: exec('global output; global = "";' + message)
        except Exception as e: await ctx.send(f'```{e}```'); return
        if len(output): await ctx.send(output)

def setup(client):
    client.add_cog(Misc(client))
