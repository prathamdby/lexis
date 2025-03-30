import asyncio
import logging
import logging.config
import os
import sys
from typing import List
import discord
from discord.ext import commands

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.config.settings import BOT_TOKEN, BOT_PREFIX, LOGGING_CONFIG
from src.utils.helpers import get_cogs_list

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True


class LexisBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or(BOT_PREFIX),
            intents=intents,
            help_command=commands.DefaultHelpCommand(),
            description="A simple Discord bot",
            activity=discord.Activity(
                type=discord.ActivityType.listening, name=f"{BOT_PREFIX}help"
            ),
        )
        self.initial_extensions: List[str] = get_cogs_list()

    async def setup_hook(self):
        for extension in self.initial_extensions:
            try:
                await self.load_extension(extension)
                logger.info(f"Loaded extension {extension}")
            except Exception as e:
                logger.error(f"Failed to load extension {extension}")

    async def on_ready(self):
        logger.info(f"Logged in as {self.user}")
        logger.info(f"Connected to {len(self.guilds)} guilds")
        try:
            await self.tree.sync()
        except Exception:
            pass

    async def on_message(self, message):
        await self.process_commands(message)

        if message.author.bot or message.content.startswith(BOT_PREFIX):
            return

        nlp_cog = self.get_cog("NLP")
        if nlp_cog:
            await nlp_cog.process_message(message)

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required argument: {error.param.name}")


async def main():
    async with LexisBot() as bot:
        if not BOT_TOKEN:
            logger.critical("No bot token found")
            return

        try:
            await bot.start(BOT_TOKEN)
        except Exception as e:
            logger.critical(f"Error starting bot: {e}")


if __name__ == "__main__":
    asyncio.run(main())
