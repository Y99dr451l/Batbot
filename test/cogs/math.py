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
        else: await ctx.send(f'The prime factors of {verification} are {factors}') 

def setup(client):
    client.add_cog(Math(client))