import discord
from discord.ext import commands, tasks
import logging

logger = logging.getLogger(__name__)


class Tasks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.status_task.start()

    def cog_unload(self):
        self.status_task.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("Tasks cog loaded")

    @tasks.loop(minutes=30)
    async def status_task(self):
        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name=f"{len(self.bot.guilds)} servers",
            )
        )

    @status_task.before_loop
    async def before_status_task(self):
        await self.bot.wait_until_ready()


async def setup(bot):
    await bot.add_cog(Tasks(bot))
