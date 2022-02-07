from io import BytesIO

import requests
import discord
import numpy
import PIL.Image
import PIL.ImageOps
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
        'edge': [[0,-1,0],[-1,4,-1],[0,-1,0]],
        'edge2': [[-1,-1,-1],[-1,8,-1],[-1,-1,-1]],
        'sharp': [[0,-1,0],[-1,5,-1],[0,-1,0]],
        'boxblur': 1/9*numpy.ones((3,3), dtype=float),
        'gaussblur': 1/16*numpy.array([[1.,2.,1.],[2.,4.,2.],[1.,2.,1.]], dtype=float),
        'emboss': [[-2,-1,0],[-1,1,1],[0,1,2]],
    }
    
    def arguments(self):
        output = 'Possible arguments are: `'
        for key in self.kernels.keys(): output += key + '`, `'
        output = output[:-3]+'.'
        return output

    @commands.command()
    async def image(self, ctx, arg=None):
        # kernel
        if arg == None: await ctx.send('Argument missing.\n'+self.arguments()); return
        if arg == 'random': kernel = self.rng.integers(-5, 5, (3, 3))
        else:
            try: kernel = self.kernels[arg]
            except: await ctx.send('Argument not valid.\n'+self.arguments()); return
        # image
        if len(ctx.message.attachments) == 0 or 'image' not in ctx.message.attachments[0].content_type:
            await ctx.send('No valid attachment found, using your avatar as input.')
            url = str(ctx.message.author.avatar_url)
            if '.gif' in url: await ctx.send('Your avatar is a gif and cannot be used.'); return
            response = requests.get(url)
            try: image_input = PIL.Image.open(BytesIO(response.content))
            except Exception as e: await ctx.send(f"Couldn't read image.\n```{e}```"); return
        else:
            input = await ctx.message.attachments[0].read()
            try: image_input = PIL.Image.open(BytesIO(input))
            except Exception as e: await ctx.send(f"Couldn't read image.\n```{e}```"); return
        # processing
        try:
            image_array = numpy.array(PIL.ImageOps.grayscale(image_input))
            data = convolve(image_array, kernel)
            image_output = PIL.Image.fromarray(data)
            bytes = BytesIO()
            image_output.save(bytes, 'PNG')
            bytes.seek(0)
            await ctx.send(content='```'+str(kernel)+'```', file=discord.File(bytes, filename='output.png'))
        except Exception as e: ctx.send(f'Error during processing.\n```{e}```'); return

def setup(client):
    client.add_cog(Image(client))
