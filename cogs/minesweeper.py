import discord
from discord.ext import commands
import numpy

class Minesweeper(commands.Cog):
        
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self} loaded.')

    field = [[]]
    visible = [[]]
    dimx = 0
    dimy = 0
    mines = 0
    rng = numpy.random.default_rng()
    emojis = [':zero:', ':one:', ':two:',
    ':three:', ':four:', ':five:', ':six:',
    ':seven:', ':eight:', ':bomb:', ':fog:']

    @commands.command(aliases = ['ms'])
    async def minesweeper(self, ctx, dimx, dimy, mines):
        self.dimx = int(dimx)
        self.dimy = int(dimy)
        self.mines = int(mines)
        if (self.dimx or self.dimy or self.mines) < 0:
            await ctx.send('Negative terms.')
            return
        if (self.dimx or self.dimy) < 2:
            await ctx.send('Dimensions too small.')
            return
        if self.mines > self.dimx * self.dimy:
            await ctx.send('Too many mines.')
            return
        self.field = [[0 for j in range(0, self.dimy+2)] for i in range(0, self.dimx+2)]
        self.visible = [[False for j in range(0, self.dimy+2)] for i in range(0, self.dimx+2)]
        i = 0
        while i < self.mines:
            rx = self.rng.integers(1, self.dimx)
            ry = self.rng.integers(1, self.dimy)
            if not self.field[ry][rx] == 9:
                self.field[ry][rx] = 9
                i += 1
        #print('mines placed')
        for j in range (1, self.dimy+1):
            for i in range (1, self.dimx+1):
                if not self.field[j][i] == 9:
                    mcount = 0
                    for k in range (-1, 2):
                        for l in range (-1, 2):
                            if self.field[j+k][i+l] == 9: mcount += 1
                    self.field[j][i] = mcount
                    #print(mcount)
        await self.msdisplay(ctx)

    @commands.command(aliases = ['msd'])
    async def msdisplay(self, ctx):
        outputstr = ''
        for j in range(1, self.dimy+1):
            for i in range(1, self.dimx+1):
                if self.visible[j][i]: outputstr += self.emojis[self.field[j][i]]
                else: outputstr += self.emojis[10]
            outputstr += '\n'
        #print(outputstr)
        if len(outputstr) > 2000:
            outputstr = 'Not using emojis because of the character limit.\n```'
            for j in range(1, self.dimy+1):
                for i in range(1, self.dimx+1):
                    if self.visible[j][i]:
                        if self.field[j][i] == 9: outputstr += '*'
                        elif self.field[j][i] == 0: outputstr += ' '
                        else: outputstr += self.field[j][i]
                    else: outputstr += 'X'
                outputstr += '\n'
            outputstr += '```'
            #print(outputstr)
        if len(outputstr) > 2000: outputstr = 'The grid is too big to be sent in one message.. adding splitting function <:soontm:859533054455971860>.'
        #print(outputstr)
        await ctx.send(outputstr)

    @commands.command(aliases = ['msm'])
    async def msmove(self, ctx, strmovex, strmovey):
        movex = int(strmovex)
        movey = int(strmovey)
        if (movex or movey) < 1 or movex > self.dimx or movey > self.dimy:
            await ctx.send('Coordinates out of bounds.')
            return
        if self.visible[movey][movex]:
            await ctx.send('Cell already uncovered.')
            return
        if self.field[movey][movex] == 9:
            await ctx.send('GAME OVER - You died.')
            self.visible = [[True for j in range(0, self.dimy+2)] for i in range(0, self.dimx+2)]
        else: self.reveal(movey, movex)
        await self.msdisplay(ctx)

    def reveal(self, movey, movex):
        self.visible[movey][movex] = True
        if not self.field[movey][movex]:
            for i in range(-1,2):
                for j in range(-1,2):
                    self.reveal[movey+j][movex+i]


def setup(client):
    client.add_cog(Minesweeper(client))
