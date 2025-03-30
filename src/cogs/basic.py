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
        temp_msg = await ctx.send("Pinging...")
        end_time = time.time()

        gateway_latency = round(self.bot.latency * 1000)
        api_latency = round((end_time - start_time) * 1000)
        await temp_msg.delete()

        fields = [
            {
                "name": "Gateway Latency",
                "value": f"`{gateway_latency}ms`",
                "inline": True,
            },
            {
                "name": "API Response Time",
                "value": f"`{api_latency}ms`",
                "inline": True,
            },
        ]

        status = (
            "✅ All Systems Operational"
            if gateway_latency < 300 and api_latency < 300
            else "⚠️ High Latency"
        )
        await send_embed(
            ctx,
            "System Status",
            status,
            discord.Color.green() if "✅" in status else discord.Color.orange(),
            "🔍",
            fields,
        )


async def setup(bot):
    await bot.add_cog(Basic(bot))
