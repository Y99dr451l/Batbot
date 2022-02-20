from io import BytesIO

import discord
import numpy
import PIL.Image
import PIL.ImageOps
import requests
from discord.ext import commands
from scipy.ndimage import convolve


class Image(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Cog {self} loaded.')

    rng = numpy.random.default_rng()
    kernels = {
        'edge': numpy.array([[0,-1,0],[-1,4,-1],[0,-1,0]]),
        'edge2': numpy.array([[-1,-1,-1],[-1,8,-1],[-1,-1,-1]]),
        'sharp': numpy.array([[0,-1,0],[-1,5,-1],[0,-1,0]]),
        'boxblur': 1/9*numpy.ones((3,3), dtype=float),
        'gaussblur': 1/16*numpy.array([[1.,2.,1.],[2.,4.,2.],[1.,2.,1.]], dtype=float),
        'emboss': numpy.array([[-2,-1,0],[-1,1,1],[0,1,2]]),
    }
    
    def arguments(self):
        output = 'Possible arguments are: `'
        for key in self.kernels.keys(): output += key + '`, `'
        output = output[:-3]+', `random` and `randomnorm`.'
        return output

    @commands.command()
    async def image(self, ctx, arg=None):
        # kernel
        if arg == None: await ctx.send('Argument missing.\n'+self.arguments()); return
        if 'random' in arg:
            kernel = self.rng.integers(-5, 5, (3, 3))
            if 'norm' in arg:
                sum = numpy.sum(kernel)
                kernel = kernel/sum if sum != 0 else kernel
        else:
            try: kernel = self.kernels[arg]
            except: await ctx.send('Argument not valid.\n'+self.arguments()); return
        # image
        if len(ctx.message.attachments) and 'image' in ctx.message.attachments[0].content_type:
            try:
                input = await ctx.message.attachments[0].read()
                image_input = PIL.Image.open(BytesIO(input))
            except Exception as e: await ctx.send(f"Couldn't read image.\n```{e}```"); return
        elif ctx.message.reference is not None: 
            try:
                input = await ctx.message.reference.cached_message.attachments[0].read()
                image_input = PIL.Image.open(BytesIO(input))
            except Exception as e: await ctx.send(f"Couldn't read referenced image.\n```{e}```"); return
        else:
            await ctx.send('No valid attachment found, using your avatar as input.')
            url = str(ctx.message.author.avatar_url)
            if '.gif' in url: await ctx.send('Your avatar is a gif and cannot be used.'); return
            response = requests.get(url)
            try:
                image_input = PIL.Image.open(BytesIO(response.content))
            except Exception as e: await ctx.send(f"Couldn't read avatar.\n```{e}```"); return            
        # processing
        try:
            image_array = numpy.array(PIL.ImageOps.grayscale(image_input))
            data = convolve(image_array, kernel)
            image_output = PIL.Image.fromarray(data)
            bytes = BytesIO()
            image_output.save(bytes, 'PNG')
            bytes.seek(0)
            await ctx.send(content='```'+str(kernel)+'```', file=discord.File(bytes, filename='output.png'))
        except Exception as e: await ctx.send(f'Error during processing.\n```{e}```'); return

def setup(client):
    client.add_cog(Image(client))
