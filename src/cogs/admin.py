import discord
from discord.ext import commands
import logging
import os  # Add os import
import sys # Add sys import
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

        fields = []
        if success:
            fields.append(
                {
                    "name": "✅ Successfully Reloaded",
                    "value": "\n".join([f"`{cog}`" for cog in success]),
                    "inline": False,
                }
            )
        if failed:
            fields.append(
                {
                    "name": "❌ Failed to Reload",
                    "value": "\n".join([f"`{cog}`" for cog in failed]),
                    "inline": False,
                }
            )

        status = "Partial Success" if failed else "Complete Success"
        color = discord.Color.orange() if failed else discord.Color.green()

        await send_embed(
            ctx,
            "Module Reload Report",
            f"Attempted to reload {len(success) + len(failed)} module(s)",
            color,
            "🔄",
            fields,
        )

    @commands.command(
        name="shutdown", description="Safely shutdown the bot and save all states"
    )
    @has_role()
    async def shutdown(self, ctx):
        fields = [
            {
                "name": "Reason",
                "value": "Administrative shutdown request",
                "inline": False,
            },
            {
                "name": "Status",
                "value": "All processes are being terminated safely",
                "inline": False,
            },
        ]

        await send_embed(
            ctx,
            "System Shutdown",
            "⚠️ Bot is shutting down. It will need to be manually restarted.",
            discord.Color.orange(),
            "🔌",
            fields,
        )
        logger.info("Bot shutting down by admin command")
        await self.bot.close()

    @commands.command(name="restart", description="Restart the bot")
    @has_role()
    async def restart(self, ctx):
        """Restarts the bot."""
        fields = [
            {
                "name": "Reason",
                "value": "Administrative restart request",
                "inline": False,
            },
            {
                "name": "Status",
                "value": "Bot is restarting...",
                "inline": False,
            },
        ]

        await send_embed(
            ctx,
            "System Restart",
            "🔄 Bot is restarting now. Please wait a moment.",
            discord.Color.blue(),
            "🔄",
            fields,
        )
        logger.info("Bot restarting by admin command...")

        await self.bot.close()

        try:
            os.execv(sys.executable, ['python'] + sys.argv)
        except Exception as e:
            logger.error(f"Failed to restart bot: {e}")
            await ctx.send(f"❌ Failed to initiate restart: {e}")


async def setup(bot):
    await bot.add_cog(Admin(bot))
