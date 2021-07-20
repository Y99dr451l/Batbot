from ..utils.checks import is_admin
from ..utils.functions import bool_switch
import discord
from discord.ext import commands

class Reactions(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    #bools
    en_lmao = 1
    en_yeet = 1
    en_bruh = 1
    en_ping = 1

    # admin commands
    @commands.command()
    @commands.check(is_admin)
    async def lmao(self, ctx, en_lmao):
        en_lmao = bool_switch(en_lmao)

    @commands.command()
    @commands.check(is_admin)
    async def yeet(self, ctx, en_yeet):
        en_yeet = bool_switch(en_yeet)

    @commands.command()
    @commands.check(is_admin)
    async def bruh(self, ctx, en_bruh):
        en_bruh = bool_switch(en_bruh)
    
    @commands.command(aliases = ['@ping'])
    @commands.check(is_admin)
    async def ping(self, ctx, en_ping):
        en_ping = bool_switch(en_ping)

    # events
    @commands.Cog.listener() #replacement for @client.event
    async def on_ready(self):
        print(f'Cog {self} loaded.')
    
    @commands.Cog.listener()
    async def reaction_event(self, ctx, en_lmao, en_yeet, en_bruh, en_ping):
        if "lmao" in ctx.content.lower() and en_lmao:
            if ctx.author.id == 181681253899042817: await ctx.add_reaction('<:lmaobassam:778739200257818636>')
            elif ctx.author.id == 287306245893914624: await ctx.add_reaction('<:lmaobatman:778740489960292352>')
            elif ctx.author.id == 449557998004862987: await ctx.add_reaction('<:lmaojonas:862717541780160542>')
        if "yeet" in ctx.content.lower() and en_yeet: await ctx.add_reaction('<:yeet:744153144040095784>')
        if "bruh" in ctx.content.lower() and en_bruh: await ctx.add_reaction('<:bruh:786383332035788832>')
        if '@' in ctx.content.lower() and en_ping: await ctx.add_reaction('<:pandaping:822443133139812394>')

def setup(client):
    client.add_cog(Reactions(client))
