import discord
from discord.ext import commands
import logging
from src.utils.helpers import has_role, send_embed

logger = logging.getLogger(__name__)


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Admin cog loaded")

    @commands.command(name="reload", description="Reload all cogs")
    @has_role("Bot Admin")
    async def reload_all(self, ctx):
        from src.utils.helpers import get_cogs_list

        success = []
        failed = []

        for cog in get_cogs_list():
            try:
                await self.bot.reload_extension(cog)
                success.append(cog)
            except Exception as e:
                failed.append(cog)
                logger.error(f"Failed to reload {cog}: {e}")

        if failed:
            await send_embed(
                ctx,
                "Reload Status",
                f"Reloaded {len(success)} cogs. Failed to reload {len(failed)} cogs.",
                discord.Color.orange(),
            )
        else:
            await send_embed(
                ctx,
                "Success",
                f"Reloaded all {len(success)} cogs",
                discord.Color.green(),
            )

    @commands.command(name="shutdown", description="Shutdown the bot")
    @has_role("Bot Admin")
    async def shutdown(self, ctx):
        await send_embed(
            ctx, "Shutting Down", "The bot is shutting down...", discord.Color.orange()
        )
        logger.info("Bot shutting down by admin command")
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(Admin(bot))
