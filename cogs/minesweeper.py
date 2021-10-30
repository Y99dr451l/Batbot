import discord
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
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
    running = False
    revealed = 0
    toreveal = 0
    rng = numpy.random.default_rng()
    emojis = [':zero:', ':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':bomb:', ':fog:', ':flag_black:']

    @commands.command(aliases = ['ms'])
    async def minesweeper(self, ctx, dimx=None, dimy=None, mines=None):
        if (dimx or dimy or mines) == None:
            await ctx.send('The necessary arguments are `dimx`, `dimy`and `mines`, in that order.')
            return
        self.running = False
        self.revealed = 0
        try:
            self.dimx = int(dimx)
            self.dimy = int(dimy)
            self.mines = int(mines)
        except ValueError:
            raise MissingRequiredArgument
        if (self.dimx or self.dimy or self.mines) < 0:
            await ctx.send('Negative terms.')
            return
        if (self.dimx or self.dimy) < 2:
            await ctx.send('Dimensions too small.')
            return
        if self.mines > self.dimx * self.dimy:
            await ctx.send('Too many mines.')
            return
        self.visible = [[0 for j in range(0, self.dimy+2)] for i in range(0, self.dimx+2)]
        i = 0
        if self.mines <= 0.5*self.dimx*self.dimy:
            self.field = [[0 for j in range(0, self.dimy+2)] for i in range(0, self.dimx+2)]
            while i < self.mines:
                rx = self.rng.integers(1, self.dimx)
                ry = self.rng.integers(1, self.dimy)
                if not self.field[ry][rx] == 9:
                    self.field[ry][rx] = 9
                    i += 1
        else:
            self.field = [[9 for j in range(0, self.dimy+2)] for i in range(0, self.dimx+2)]
            while i < self.dimx*self.dimy-self.mines:
                rx = self.rng.integers(1, self.dimx)
                ry = self.rng.integers(1, self.dimy)
                if not self.field[ry][rx] == 0:
                    self.field[ry][rx] = 0
                    i += 1
        for j in range (1, self.dimy+1):
            for i in range (1, self.dimx+1):
                if not self.field[j][i] == 9:
                    mcount = 0
                    for k in range (-1, 2):
                        for l in range (-1, 2):
                            if self.field[j+k][i+l] == 9: mcount += 1
                    self.field[j][i] = mcount
        self.running = True
        self.toreveal = self.dimx*self.dimy-self.mines
        await self.msdisplay(ctx)

    @commands.command(aliases = ['msd'])
    async def msdisplay(self, ctx):
        outputstr = ''
        for j in range(1, self.dimy+1):
            for i in range(1, self.dimx+1):
                if self.visible[j][i] == 1: outputstr += self.emojis[self.field[j][i]]
                elif self.visible[j][i] == 2: outputstr += self.emojis[11]
                else: outputstr += self.emojis[10]
            outputstr += '\n'
        if len(outputstr) > 2000:
            outputstr = ''
            for j in range(1, self.dimy+1):
                for i in range(1, self.dimx+1):
                    if self.visible[j][i] == 1:
                        if self.field[j][i] == 9: outputstr += '*'
                        elif self.field[j][i] == 0: outputstr += ' '
                        else: outputstr += self.field[j][i]
                    elif self.visible[j][i] == 2: outputstr += 'F'
                    else: outputstr += 'X'
                outputstr += '\n'
            outputstr += '```'
        if len(outputstr) > 2000: outputstr = 'The grid is too big to be sent in one message.. adding splitting function <:soontm:859533054455971860>.'
        await ctx.send(outputstr)

    @commands.command(aliases = ['msm'])
    async def msmove(self, ctx, strmovex=None, strmovey=None):
        if strmovex == None:
            await ctx.send('The necessary arguments are `x` and `y`.\nThe x-axis goes from left to right and the y-axis from top to bottom, both starting at 1.')
            return
        if not self.running:
            await ctx.send('No game is running. Start one with the `ms`-command.')
            return
        try:
            movex = int(strmovex)
            movey = int(strmovey)
        except ValueError:
            raise MissingRequiredArgument
        if (movex or movey) < 1 or movex > self.dimx or movey > self.dimy:
            await ctx.send('Coordinates out of bounds.')
            return
        if self.visible[movey][movex] == 1:
            fcount = 0
            for i in range(movex-1, movex+2):
                for j in range(movey-1, movey+2):
                    if self.visible[j][i] == 2: fcount += 1
            if fcount == self.field[movey][movex]:
                for i in range(movex-1, movex+2):
                    for j in range(movey-1, movey+2):
                        if not self.visible[j][i]: self.reveal(j, i)
        if self.field[movey][movex] == 9:
            await ctx.send('GAME OVER - You died. :dizzy_face:')
            self.visible = [[1 for j in range(0, self.dimy+2)] for i in range(0, self.dimx+2)]
            self.running = False
        else: self.reveal(movey, movex)
        if self.revealed == self.toreveal and self.running:
            await ctx.send('GAME OVER - You won! :sunglasses:')
            self.visible = [[1 for j in range(0, self.dimy+2)] for i in range(0, self.dimx+2)]
            self.running = False
        await self.msdisplay(ctx)

    def reveal(self, movey, movex):
        self.visible[movey][movex] = 1
        self.revealed += 1
        if not self.field[movey][movex]:
            for i in range(movex-1, movex+2):
                for j in range(movey-1, movey+2):
                    if i in range(1, self.dimx+1) and j in range(1, self.dimy+1) and not self.visible[j][i]: self.reveal(j, i)

    @commands.command(aliases = ['msf'])
    async def msflag(self, ctx, strmovex, strmovey):
        movex = int(strmovex)
        movey = int(strmovey)
        if (movex or movey) < 1 or movex > self.dimx or movey > self.dimy:
            await ctx.send('Coordinates out of bounds.')
            return
        if self.visible[movey][movex] == 1:
            ccount = 0
            for i in range(movex-1, movex+2):
                for j in range(movey-1, movey+2):
                    if not self.visible[j][i]: ccount += 1
            if ccount == self.field[movey][movex]:
                for i in range(movex-1, movex+2):
                    for j in range(movey-1, movey+2):
                        if not self.visible[j][i]: self.visible[j][i] = 2
        else: self.visible[movey][movex] = 0 if self.visible[movey][movex] == 2 else 2
        await self.msdisplay(ctx)

def setup(client):
    client.add_cog(Minesweeper(client))