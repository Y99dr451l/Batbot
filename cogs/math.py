import discord
from discord.ext import commands
import math

class Math(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self} loaded.')

    @commands.command(aliases = ['pf'])
    async def prime(self, ctx, number):
        n = int(number)
        verification = int(number)
        i = 2
        factors = []
        while i * i <= n:
            if n % i: i += 1
            else:
                n //= i
                factors.append(i)
        if n > 1: factors.append(n)
        if verification in factors: await ctx.send(f'{verification} is a prime number!')
        else: await ctx.send(f'The prime factors of {verification} are '+f'{factors}'[1:-1])
    
    @commands.command(aliases = ['seq'])
    async def sequence(self, ctx, seqstr=None, numberstr=None):
        if seqstr == None:
            await ctx.send('The possible arguments currently are `fibonacci`and `conway`.')
            return
        if numberstr == None:
            await ctx.send('Give the amount of steps when calling the command.')
            return
        steps = int(numberstr)
        if seqstr == 'fibonacci' or seqstr == 'fib' or seqstr == 'f':
            if steps > 2000:
                await ctx.send('Too many steps.')
                return
            fibnew = 1
            fibold = 0
            outputstr = f'{fibnew}, '
            for i in range(2, steps+1):
                temp = fibnew
                fibnew += fibold
                fibold = temp
                if steps <= 128: outputstr += f'{fibnew}, '
            outputstr = outputstr[:-2]
            if steps > 128: outputstr = f'The {steps}th number in the Fibonacci sequence is {fibnew}.'
            await ctx.send(outputstr)
        elif seqstr == 'conway' or seqstr == 'con' or seqstr == 'c':
            if steps > 200:
                await ctx.send('Too many steps.')
                return
            connew = '1'
            outputstr = connew + ', '
            for i in range(2, steps+1):
                conold = connew
                connew = ''
                while len(conold) > 0:
                    j = 1
                    while j < len(conold) and conold[j] == conold[0]: j += 1
                    connew += f'{j}'+conold[0]
                    conold = conold[int(j):]
                outputstr += connew + ', '
            outputstr = outputstr[:-2]
            if len(outputstr) > 2000: outputstr = f'The {steps}th number in the Conway sequence is ' + connew + '.'
            await ctx.send(outputstr)

def setup(client):
    client.add_cog(Math(client))