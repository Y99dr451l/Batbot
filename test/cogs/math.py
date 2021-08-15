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
        output = f'The prime factors of {int(input)} are '
        number = input
        i = 2
        while i < math.sqrt(input):
            if number % i == 0:
                number = number / i
                output = output + f'{i}, '
            else: i += 1
        if number == input: output = f'{int(input)} is a prime number!'
        else: output = output[:-2] + f' and {int(number)}.'
        await ctx.send(output)

def setup(client):
    client.add_cog(Math(client))