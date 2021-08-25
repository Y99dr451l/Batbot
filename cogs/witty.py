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
    wittwer3 = numpy.zeros(9)
    wittwer4 = numpy.zeros(16)
    w3b = 0
    w3z = 0
    w4b = 0
    w4z = 0
    emojis3 = [
        '<:39:860269430537060382>', '<:38:860269430562095104>', '<:37:860269430490791966>',
        '<:36:860269430580051978>', '<:35:860269430629990412>', '<:34:860269430406381649>',
        '<:33:860269430466674728>', '<:32:860269430369550337>', '<:0_:859762589503586304>',
        '<:31:860269430385541120>'
    ]
    emojis4 = [
        '<:16:859536749982253076>', '<:15:859536749582745611>', '<:14:859536749708574721>', '<:13:859536749897056287>',
        '<:12:859536749922091068>', '<:11:859536749982384168>', '<:10:859536749909770280>', '<:9_:859536749825622067>',
        '<:8_:859536749624557569>', '<:7_:859536749897056286>', '<:6_:859536749646839829>', '<:5_:859536749850918963>',
        '<:4_:859536749835452416>', '<:3_:859536749796786215>', '<:2_:859536749838991420>', '<:0_:859762589503586304>',
        '<:1_:859536749830471740>'
    ]
    mixedstr = 'Wittwer has been mixed.'
    remixedstr = 'Wittwer was already mixed, remixing now.'
    unmixedstr = 'Wittwer isn\'t mixed yet.'
    invalidmovestr = 'This is not a valid move.'
    winstr = 'You won!'

    @commands.command()
    async def wmix3(self, ctx):
        if self.w3b == 1 or self.w4b == 1: await ctx.send(self.remixedstr)
        self.w3b = 1
        self.w4b = 0
        self.wittwer3 = numpy.arange(9)
        self.rng.shuffle(self.wittwer3)
        reshfl = 0
        while _af_parity(self.wittwer3):
            self.rng.shuffle(self.wittwer3)
            reshfl += 1
        for n in range(0, 9):
            if self.wittwer3[n] == 8:
                self.w3z = n
                break
        await ctx.send(self.printw3(self.wittwer3))
        reshflstr = self.mixedstr+'\nThe grid has been reshuffled '+str(reshfl)+' times.'
        if reshfl == 1: reshflstr = reshflstr[:-2] + '.'
        await ctx.send(reshflstr)

    @commands.command()
    async def wmix4(self, ctx):
        if self.w3b == 1 or self.w4b == 1: await ctx.send(self.remixedstr)
        self.w3b = 0
        self.w4b = 1
        self.wittwer4 = numpy.arange(16)
        self.rng.shuffle(self.wittwer4)
        reshfl = 0
        while _af_parity(self.wittwer4):
            self.rng.shuffle(self.wittwer4)
            reshfl += 1
        for n in range(0, 16):
            if self.wittwer4[n] == 15:
                w4z = n
                break
        await ctx.send(self.printw4(self.wittwer4))
        reshflstr = self.mixedstr+'\nThe grid has been reshuffled '+str(reshfl)+' times.'
        if reshfl == 1: reshflstr = reshflstr[:-2] + '.'
        await ctx.send(reshflstr)

    @commands.command(aliases = ['m'])
    async def move(self, ctx, moves):
        if set(moves).issubset({'u','d','l','r'}):
            if self.w3b == self.w4b:
                if self.w3b == 1:
                    w3b = 0
                    w4b = 0
                await ctx.send(self.unmixedstr)
                return
            error = 0
            l = 0
            if self.w3b == 1 and self.w4b == 0:
                while error == 0 and l < len(moves):
                    input2 = moves[l]
                    if input2 == 'r':
                        if self.w3z == 0 or self.w3z == 3 or self.w3z == 6: error = 1
                        else:
                            temp = self.wittwer3[self.w3z - 1]
                            self.wittwer3[self.w3z - 1] = self.wittwer3[self.w3z]
                            self.wittwer3[self.w3z] = temp
                            self.w3z -= 1
                    elif input2 == 'l':
                        if self.w3z == 2 or self.w3z == 5 or self.w3z == 8: error = 1
                        else:
                            temp = self.wittwer3[self.w3z + 1]
                            self.wittwer3[self.w3z + 1] = self.wittwer3[self.w3z]
                            self.wittwer3[self.w3z] = temp
                            self.w3z += 1
                    elif input2 == 'd':
                        if self.w3z == 0 or self.w3z == 1 or self.w3z == 2: error = 1
                        else:
                            temp = self.wittwer3[self.w3z - 3]
                            self.wittwer3[self.w3z - 3] = self.wittwer3[self.w3z]
                            self.wittwer3[self.w3z] = temp
                            self.w3z -= 3
                    elif input2 == 'u':
                        if self.w3z == 6 or self.w3z == 7 or self.w3z == 8: error = 1
                        else:
                            temp = self.wittwer3[self.w3z + 3]
                            self.wittwer3[self.w3z + 3] = self.wittwer3[self.w3z]
                            self.wittwer3[self.w3z] = temp
                            self.w3z += 3
                    l += 1
                if error == 1: await ctx.send(self.invalidmovestr)
                await ctx.send(self.printw3(self.wittwer3))
                cnt = 0
                for n in range(9):
                    if self.wittwer3[n] == n: cnt += 1
                if cnt == 9:
                    error = 1
                    w4b = 0
                    await ctx.send(self.winstr)
                return  
            """ elif w3b == 0 and w4b == 1:
                while error == 0 and l < len(input):
                    input2 = input[l]
                    if input2 == 'r':
                        if w4z == 0 or w4z == 4 or w4z == 8 or w4z == 12: error = 1
                        else:
                            temp = wittwer4[w4z - 1]
                            wittwer4[w4z - 1] = wittwer4[w4z]
                            wittwer4[w4z] = temp
                            w4z -= 1
                    if input2 == 'l' and error == 0:
                        if w4z == 3 or w4z == 7 or w4z == 11 or w4z == 15: error = 1
                        else:
                            temp = wittwer4[w4z + 1]
                            wittwer4[w4z + 1] = wittwer4[w4z]
                            wittwer4[w4z] = temp
                            w4z += 1
                    if input2 == 'd' and error == 0:
                        if w4z == 0 or w4z == 1 or w4z == 2 or w4z == 3: error = 1
                        else:
                            temp = wittwer4[w4z - 4]
                            wittwer4[w4z - 4] = wittwer4[w4z]
                            wittwer4[w4z] = temp
                            w4z -= 4
                    if input2 == 'u' and error == 0:
                        if w4z == 12 or w4z == 13 or w4z == 14 or w4z == 15: error = 1
                        else:
                            temp = wittwer4[w4z + 4]
                            wittwer4[w4z + 4] = wittwer4[w4z]
                            wittwer4[w4z] = temp
                            w4z += 4
                    l += 1
                if error == 1: await message.channel.send(invalidmovestr)
                await message.channel.send(printw4(wittwer4))
                cnt = 0
                for n in range(16):
                    if wittwer4[n] == n: cnt += 1
                if cnt == 16:
                    error = 1
                    w4b = 0
                    await message.channel.send(winstr+winstr4)
                return """
        else: await ctx.send(self.invalidmovestr)

    # functions
    def printw3(self, arrayinput):
        ppwstr = ''
        cnt = 0
        for n in range(9):
            ppwstr += self.emojis3[arrayinput[n]]
            cnt += 1
            if cnt == 3:
                cnt = 0
                ppwstr += '\n'
        return ppwstr

    """ def printw4(self, arrayinput):
        ppwstr = ''
        cnt = 0
        for n in range(16):
            ppwstr += self.emojis4[arrayinput[n]]
            cnt += 1
            if cnt == 4:
                cnt = 0
                ppwstr += '\n'
        return ppwstr """

def setup(client):
    client.add_cog(Witty(client))