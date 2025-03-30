import discord
from discord.ext import commands
import logging
import time

logger = logging.getLogger(__name__)


class Basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Basic cog loaded")

    @commands.command(
        name="ping", description="Check the bot's connection health and response times"
    )
    async def ping(self, ctx):
        start_time = time.time()
        message = await ctx.send("Pinging...")
        end_time = time.time()

        await message.edit(
            content=f"🟢 System Status:\n• Gateway Latency: {round(self.bot.latency * 1000)}ms\n• API Response Time: {round((end_time - start_time) * 1000)}ms"
        )


async def setup(bot):
    await bot.add_cog(Basic(bot))
