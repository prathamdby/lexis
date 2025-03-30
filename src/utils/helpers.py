import os
import discord
from discord.ext import commands


def get_cogs_list():
    cogs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cogs")
    cogs = []
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and not filename.startswith("_"):
            cogs.append(f"src.cogs.{filename[:-3]}")
    return cogs


async def send_embed(ctx, title, description, color=discord.Color.blue()):
    embed = discord.Embed(title=title, description=description, color=color)
    await ctx.send(embed=embed)


def has_role(role_name):
    async def predicate(ctx):
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is None:
            return False
        return role in ctx.author.roles

    return commands.check(predicate)
