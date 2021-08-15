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
    async def prime(ctx, input):
        output = f'The prime factors of {input} are '
        number = input
        for i in range(2, math.sqrt(input)):
            if number % i == 0:
                number = number / i
                output = output + f'{i}, '
                i = i - 1
        if number == input:
            await ctx.send(f'{input} is a prime number!')
        else: await ctx.send(output[:-2] + f' and {number}.')

def setup(client):
    client.add_cog(Math(client))