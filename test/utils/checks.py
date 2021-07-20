import discord
from data import admins

def is_admin(ctx, admins):
    return ctx.author.id in admins