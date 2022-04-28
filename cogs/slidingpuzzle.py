import discord
from discord.ext import commands
from discord.ext.commands import is_owner
import numpy
from sympy.combinatorics.permutations import _af_parity

class SlidingPuzzle(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self} loaded.')

    rng = numpy.random.default_rng()
    grid = numpy.zeros(9)
    started = False
    zeropos = 0
    witty = False
    emojis = [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':white_large_square:',
            '<:39:860269430537060382>', '<:38:860269430562095104>', '<:37:860269430490791966>',
            '<:36:860269430580051978>', '<:35:860269430629990412>', '<:34:860269430406381649>',
            '<:33:860269430466674728>', '<:32:860269430369550337>', '<:0_:859762589503586304>'
    ]
    mixedstr = 'The grid has been mixed.'
    remixedstr = 'The grid was already mixed, remixing now.'
    unmixedstr = 'The grid isn\'t mixed yet.'
    invalidmovestr = 'This is not a valid move; valid moves are a sequence of the letters u, d, l and r.'
    winstr = 'You won!'

    @commands.command(aliases = ['sp'])
    async def slidingpuzzle(self, ctx):
        if self.started: await ctx.send(self.remixedstr)
        self.started = True
        self.grid = numpy.arange(9)
        self.rng.shuffle(self.grid)
        reshfl = 0
        while _af_parity(self.grid):
            self.rng.shuffle(self.grid)
            reshfl += 1
        for n in range(0, 9):
            if self.grid[n] == 8:
                self.zeropos = n
                break
        await self.spdisplay(ctx)
        reshflstr = self.mixedstr+'\nThe grid has been reshuffled '+str(reshfl)+' times.'
        if reshfl == 1: reshflstr = reshflstr[:-2] + '.'
        await ctx.send(reshflstr)

    @commands.command(aliases = ['spm'])
    async def spmove(self, ctx, moves):
        if self.started == 0:
            await ctx.send(self.unmixedstr)
            return
        if set(moves).issubset({'u','d','l','r'}):
            error = False
            l = 0
            while error == False and l < len(moves):
                input2 = moves[l]
                if input2 == 'r':
                    if self.zeropos == 0 or self.zeropos == 3 or self.zeropos == 6: error = 1
                    else:
                        temp = self.grid[self.zeropos - 1]
                        self.grid[self.zeropos - 1] = self.grid[self.zeropos]
                        self.grid[self.zeropos] = temp
                        self.zeropos -= 1
                elif input2 == 'l':
                    if self.zeropos == 2 or self.zeropos == 5 or self.zeropos == 8: error = 1
                    else:
                        temp = self.grid[self.zeropos + 1]
                        self.grid[self.zeropos + 1] = self.grid[self.zeropos]
                        self.grid[self.zeropos] = temp
                        self.zeropos += 1
                elif input2 == 'd':
                    if self.zeropos == 0 or self.zeropos == 1 or self.zeropos == 2: error = 1
                    else:
                        temp = self.grid[self.zeropos - 3]
                        self.grid[self.zeropos - 3] = self.grid[self.zeropos]
                        self.grid[self.zeropos] = temp
                        self.zeropos -= 3
                elif input2 == 'u':
                    if self.zeropos == 6 or self.zeropos == 7 or self.zeropos == 8: error = 1
                    else:
                        temp = self.grid[self.zeropos + 3]
                        self.grid[self.zeropos + 3] = self.grid[self.zeropos]
                        self.grid[self.zeropos] = temp
                        self.zeropos += 3
                l += 1
            if error == True: await ctx.send(self.invalidmovestr)
            await self.spdisplay(ctx)
            cnt = 0
            for n in range(9):
                if self.grid[n] == n: cnt += 1
            if cnt == 9:
                error = True
                self.started = False
                await ctx.send(self.winstr)
            return  
        else: await ctx.send(self.invalidmovestr)

    @commands.command(aliases = ['spd'])
    async def spdisplay(self, ctx):
        outputstr = ''
        cnt = 0
        offset = 9 if self.witty else 0
        for n in range(9):
            outputstr += self.emojis[self.grid[n]+offset]
            cnt += 1
            if cnt == 3:
                cnt = 0
                outputstr += '\n'
        await ctx.send(outputstr)

    @commands.command(aliases = ['spw'])
    @is_owner()
    async def spwitty(self, ctx):
        self.witty = not self.witty
        await ctx.send(f'Witty: {self.witty}')

def setup(client):
    client.add_cog(SlidingPuzzle(client))