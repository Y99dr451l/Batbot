import discord
from test.utils.data import admins

def is_admin(ctx, admins):
    return ctx.author.id in admins