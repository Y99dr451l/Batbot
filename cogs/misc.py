import discord
from discord.ext import commands
from discord.ext.commands import is_owner
import requests
import json
import time

class Misc(commands.Cog):

    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self} loaded.')
        self.starttime = time.monotonic()

    @commands.command(aliases = ['up', 'ut'])
    async def uptime(self, ctx):
        if not self.starttime:
            self.starttime = time.monotonic()
            await ctx.send('starttime has been set now.')
        uptime = time.monotonic()-self.starttime
        utdys = uptime//(3600*24)
        uthrs = uptime//3600-utdys*24
        utmin = uptime//60-uthrs*60-utdys*60*24
        utsec = uptime-utmin*60-uthrs*3600-utdys*3600*24
        output = 'The bot has been up for '
        if utdys: output += f'{int(utdys)} days, '
        if uthrs: output += f'{int(uthrs)} hours, '
        if utmin: output += f'{int(utmin)} minutes, '
        await ctx.send(output + f'{round(utsec,4)} seconds.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        print(f'{member} has left a server.')

    @commands.command(aliases = ['lat', 'ping'])
    async def latency(self, ctx):
        await ctx.send(f'{round(self.client.latency*1000,4)}ms')

    @commands.command(aliases = ['zq', 'quote'])
    async def zenquote(self, ctx):
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        await ctx.send(json_data[0]["q"]+'\n- '+json_data[0]["a"])

def setup(client):
    client.add_cog(Misc(client))
