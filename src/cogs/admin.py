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

    @commands.command(
        name="reload", description="Reload all bot modules to apply code changes"
    )
    @has_role()
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
                "Module Reload Status",
                f"Successfully reloaded {len(success)} modules. {len(failed)} modules failed to reload. Check logs for details.",
                discord.Color.orange(),
            )
        else:
            await send_embed(
                ctx,
                "Modules Reloaded",
                f"Successfully reloaded all {len(success)} bot modules",
                discord.Color.green(),
            )

    @commands.command(
        name="shutdown", description="Safely shutdown the bot and save all states"
    )
    @has_role()
    async def shutdown(self, ctx):
        await send_embed(
            ctx,
            "Shutdown Initiated",
            "The bot is shutting down safely. All processes will be terminated.",
            discord.Color.orange(),
        )
        logger.info("Bot shutting down by admin command")
        await self.bot.close()


async def setup(bot):
    await bot.add_cog(Admin(bot))
