import discord
from discord.ext import commands
from discord.ext.commands import is_owner

class Send(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.last = {
            'channel': None,
            'message': None,
            'user': None,
        }

    @commands.command()
    @is_owner()
    async def set(self, ctx):
        message = ctx.message.content[5:]
        id = message[-18:]
        type = message[:-19]
        if id.isdecimal() and type in self.last.keys():
            self.last[type] = int(id)

    @commands.command()
    @is_owner()
    async def sendinfo(self, ctx):
        channelstr = 'None'
        messagestr = 'None'
        userstr = 'None'
        if self.last['channel']:
            try:
                channel = await self.client.fetch_channel(self.last['channel'])
                channelstr = f'{channel.name} in {channel.guild.name}'
            except Exception as e: channelstr = f'`{e}`'
        if self.last['message']:
            try:
                message = await channel.fetch_message(self.last['message'])
                messagestr = f'"{message.content[:20]}" by {message.author.name}'
            except Exception as e: messagestr = f'`{e}`'
        if self.last['user']:
            try:
                user = await self.client.fetch_user(self.last['user'])
                userstr = f'{user}'
            except Exception as e: userstr = f'`{e}`'
        await ctx.send(f'Channel: {channelstr}\nMessage: {messagestr}\nUser: {userstr}')

    @commands.command()
    @is_owner()
    async def send(self, ctx):
        message = ctx.message.content[6:]
        if self.last['user']:
            channel = self.client.fetch_channel(self.last['channel'])
            await channel.send(message)
        else: await ctx.send("No channel set.")

    @commands.command(name = '+')
    @is_owner()
    async def react(self, ctx):
        emoji = ctx.message.content[3:]
        if self.last['channel']:
            try: channel = self.client.get_channel(self.last['channel'])
            except: await ctx.send("No channel found."); return
            try: dest = await channel.fetch_message(self.last['message'])
            except:
                try: dest = await channel.fetch_message(channel.last_message_id)
                except: await ctx.send("No message found."); return
            try: await dest.add_reaction(emoji)
            except:
                try:
                    emoji = discord.utils.get(channel.guild.emojis, name = emoji)
                    await dest.add_reaction(emoji)
                except: await ctx.send("No valid emoji."); return
        else: await ctx.send("No channel set.")

    @commands.command()
    @is_owner()
    async def dm(self, ctx):
        message = ctx.message.content[4:]
        if self.last['user']:
            user = self.client.get_user(self.last['user'])
            await user.send(message)
        else: await ctx.send("No user set.")

def setup(client):
    client.add_cog(Send(client))