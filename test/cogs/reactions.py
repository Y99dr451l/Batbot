# from ..utils.checks import is_admin
from ..utils.functions import bool_switch
import discord
from discord.ext import commands
from discord.ext.commands import is_owner

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
    @is_owner()
    async def rlmao(self, ctx):
        self.en_lmao = not self.en_lmao

    @commands.command()
    @is_owner()
    async def ryeet(self, ctx):
        self.en_yeet = not self.en_yeet

    @commands.command()
    @is_owner()
    async def rbruh(self, ctx):
        self.en_bruh = not self.en_bruh
    
    @commands.command()
    @is_owner()
    async def rping(self, ctx):
        self.en_ping = not self.en_ping

    # events
    @commands.Cog.listener() #replacement for @client.event
    async def on_ready(self):
        print(f'Cog {self} loaded.')
    
    @commands.Cog.listener()
    async def reaction_event(self, ctx):
        if "lmao" in ctx.content.lower() and self.en_lmao:
            if ctx.author.id == 181681253899042817: await ctx.add_reaction('<:lmaobassam:778739200257818636>')
            elif ctx.author.id == 287306245893914624: await ctx.add_reaction('<:lmaobatman:778740489960292352>')
            elif ctx.author.id == 449557998004862987: await ctx.add_reaction('<:lmaojonas:862717541780160542>')
            #else: await ctx.add_reaction('')
        if "yeet" in ctx.content.lower() and self.en_yeet: await ctx.add_reaction('<:yeet:744153144040095784>')
        if "bruh" in ctx.content.lower() and self.en_bruh: await ctx.add_reaction('<:bruh:786383332035788832>')
        if '@' in ctx.content.lower() and self.en_ping: await ctx.add_reaction('<:pandaping:822443133139812394>')

def setup(client):
    client.add_cog(Reactions(client))
