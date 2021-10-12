import discord
from discord.ext import commands
from discord.ext.commands import is_owner
import numpy

class Reactions(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self} loaded.')

    #bools
    en_lmao = True
    en_yeet = True
    en_bruh = True
    en_ping = True
    en_aaa = True

    rng = numpy.random.default_rng()

    # admin commands
    @commands.command(name = 'rc')
    @is_owner()
    async def reactions(self, ctx, argstr='.'):
        argstr = argstr.lower()
        if argstr == 'lmao': self.en_lmao = not self.en_lmao
        elif argstr == 'yeet': self.en_yeet = not self.en_yeet
        elif argstr == 'bruh': self.en_bruh = not self.en_bruh
        elif argstr == 'ping': self.en_ping = not self.en_ping
        elif argstr == 'aaa': self.en_aaa = not self.en_aaa
        await ctx.send(f'lmao: {self.en_lmao}\nyeet: {self.en_yeet}\nbruh: {self.en_bruh}\nping: {self.en_ping}\naaa: {self.en_aaa}')

    # events
    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author == self.client.user:
            content = ctx.content.lower()
            authorid = ctx.author.id
            if self.en_lmao and "lmao" in content:
                if authorid == 181681253899042817: await ctx.add_reaction('<:lmaobassam:778739200257818636>')
                elif authorid == 287306245893914624: await ctx.add_reaction('<:lmaobatman:778740489960292352>')
                elif authorid == 449557998004862987: await ctx.add_reaction('<:lmaojonas:862717541780160542>')
                else: await ctx.add_reaction('<:lmao:880102637956120577>')
            if self.en_yeet and "yeet" in content: await ctx.add_reaction('<:yeet:744153144040095784>')
            if self.en_bruh and "bruh" in content: await ctx.add_reaction('<:bruh:786383332035788832>')
            if self.en_ping and '@' in content: await ctx.add_reaction('<:pandaping:822443133139812394>')
            if self.en_aaa and self.oneletter(content) and len(content) > 2: await ctx.channel.send(content[0].upper()*min(self.rng.integers(1,50)*len(content), 2000))

    def oneletter(self, content):
        first = content[0]
        check = 1
        for i in range(1, len(content)):
            if not content[i] == first:
                check = 0
                break
        return check

def setup(client):
    client.add_cog(Reactions(client))
