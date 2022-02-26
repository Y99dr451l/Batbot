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

    bools = {
        'lmao': True,
        'yeet': True,
        'bruh': True,
        '@': True,
        'aaa': True,
        'nice': True,
    }

    lmaos = {
        181681253899042817: '<:lmaobassam:778739200257818636>',
        287306245893914624: '<:lmaobatman:778740489960292352>',
        449557998004862987: '<:lmaojonas:862717541780160542>',
        'default': '<:lmao:880102637956120577>',
    }

    reacs = {
        'yeet': '<:yeet:744153144040095784>',
        'bruh': '<:bruh:786383332035788832>',
        '@': '<:pandaping:822443133139812394>',
        'nice': '👌',
    }

    rng = numpy.random.default_rng()

    @commands.command()
    @is_owner()
    async def rc(self, ctx):
        content = ctx.message.content
        if len(content) > 4:
            argstr = content[4:].lower()
            for key in self.bools.keys():
                if key in argstr: self.bools[key] = not self.bools[key]
        output = ''
        for (key, value) in self.bools.items(): output += f'{key}: {value}\n'
        await ctx.send(output)

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if not ctx.author == self.client.user:
            content = ctx.content.lower()
            authorid = ctx.author.id
            if self.bools['lmao'] and 'lmao' in content:
                if authorid in self.lmaos.keys(): await ctx.add_reaction(self.lmaos[authorid])
                else: await ctx.add_reaction(self.lmaos['default'])
            for key in self.reacs.keys():
                if self.bools[key] and key in content: await ctx.add_reaction(self.reacs[key])
            if self.bools['aaa'] and len(content) > 2:
                first = content[0]
                check = True
                for i in range(1, len(content)):
                    if not content[i] == first: check = False; break
                if check: await ctx.channel.send(first.upper()*self.rng.integers(1,50))

def setup(client):
    client.add_cog(Reactions(client))
