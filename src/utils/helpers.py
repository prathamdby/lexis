import os
import discord
from discord.ext import commands
from src.config.settings import ADMIN_ROLE, OWNER_ID


def get_cogs_list():
    cogs_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cogs")
    cogs = []
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and not filename.startswith("_"):
            cogs.append(f"src.cogs.{filename[:-3]}")
    return cogs


async def send_embed(
    ctx, title, description, color=discord.Color.blue(), emoji="", fields=None
):
    """Create and send a standardized embed message

    Args:
        ctx: Command context
        title: Embed title
        description: Main embed description
        color: Color of the embed (default: blue)
        emoji: Optional emoji prefix for title
        fields: Optional list of fields, each being a dict with 'name' and 'value' keys
    """
    title_with_emoji = f"{emoji} {title}" if emoji else title
    embed = discord.Embed(
        title=title_with_emoji,
        description=description,
        color=color,
        timestamp=ctx.message.created_at,
    )

    if ctx.author:
        embed.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )

    if fields:
        for field in fields:
            embed.add_field(
                name=field["name"],
                value=field["value"],
                inline=field.get("inline", False),
            )

    embed.set_footer(text=f"{ctx.bot.user.name} | Use !help for commands")

    await ctx.message.reply(embed=embed)


def has_role(role_name=ADMIN_ROLE):
    async def predicate(ctx):
        if ctx.author.id == OWNER_ID:
            return True

        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role is None:
            return False
        return role in ctx.author.roles

    return commands.check(predicate)
