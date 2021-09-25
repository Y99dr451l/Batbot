import discord
from discord.ext import commands
import numpy
from sympy.combinatorics.permutations import _af_parity

class Witty(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self} loaded.')

    # variables
    rng = numpy.random.default_rng()
    grid = numpy.zeros(9)
    started = 0
    zeropos = 0

    emojis = [
        '<:39:860269430537060382>', '<:38:860269430562095104>', '<:37:860269430490791966>',
        '<:36:860269430580051978>', '<:35:860269430629990412>', '<:34:860269430406381649>',
        '<:33:860269430466674728>', '<:32:860269430369550337>', '<:0_:859762589503586304>',
        '<:31:860269430385541120>'
    ]
    mixedstr = 'Wittwer has been mixed.'
    remixedstr = 'Wittwer was already mixed, remixing now.'
    unmixedstr = 'Wittwer isn\'t mixed yet.'
    invalidmovestr = 'This is not a valid move.'
    winstr = 'You won!'

    @commands.command()
    async def wmix(self, ctx):
        if self.started == 1: await ctx.send(self.remixedstr)
        self.started = 1
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
        await ctx.send(self.printwitty(self.grid))
        reshflstr = self.mixedstr+'\nThe grid has been reshuffled '+str(reshfl)+' times.'
        if reshfl == 1: reshflstr = reshflstr[:-2] + '.'
        await ctx.send(reshflstr)

    @commands.command(aliases = ['m'])
    async def move(self, ctx, moves):
        if set(moves).issubset({'u','d','l','r'}):
            if self.started == 0:
                if self.started == 1:
                    await ctx.send(self.unmixedstr)
                    return
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
            await ctx.send(self.printwitty(self.grid))
            cnt = 0
            for n in range(9):
                if self.grid[n] == n: cnt += 1
            if cnt == 9:
                error = True
                self.started = False
                await ctx.send(self.winstr)
            return  
        else: await ctx.send(self.invalidmovestr)

    # functions
    def printwitty(self, arrayinput):
        outputstr = ''
        cnt = 0
        for n in range(9):
            outputstr += self.emojis[arrayinput[n]]
            cnt += 1
            if cnt == 3:
                cnt = 0
                outputstr += '\n'
        return outputstr

def setup(client):
    client.add_cog(Witty(client))