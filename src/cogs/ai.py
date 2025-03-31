import discord
from discord.ext import commands
import logging
from typing import List, Dict
import asyncio

from src.utils.helpers import send_embed
from src.utils.ai_client import AIClient
from src.config.settings import RATE_LIMIT_INTERVAL, RATE_LIMIT_MAX_REQUESTS

logger = logging.getLogger(__name__)


class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai_client = AIClient()
        self.nlp_cog = None
        self.active_requests = set()
        logger.info(
            f"AI cog initialized with rate limits: {RATE_LIMIT_MAX_REQUESTS} requests every {RATE_LIMIT_INTERVAL} seconds"
        )

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("AI cog loaded")
        self.nlp_cog = self.bot.get_cog("NLP")
        if not self.nlp_cog:
            logger.warning("NLP cog not found, AI Ask will have limited functionality")

    @commands.command(
        name="ask",
        description="Ask a question and get an answer based on the knowledge base",
    )
    async def ask(self, ctx, *, question: str = None):
        user_id = ctx.author.id

        if user_id in self.active_requests:
            await send_embed(
                ctx,
                "Request In Progress",
                "You already have a question being processed. Please wait for it to complete.",
                discord.Color.orange(),
                "⏳",
            )
            return

        if not question:
            await send_embed(
                ctx,
                "Missing Question",
                "Please provide a question to ask. Example: `!ask What is Discord?`",
                discord.Color.orange(),
                "❓",
            )
            return

        if not self.nlp_cog or not hasattr(self.nlp_cog, "nlp_processor"):
            await send_embed(
                ctx,
                "Knowledge Base Not Available",
                "The knowledge base is not available. Please try again later.",
                discord.Color.red(),
                "❌",
            )
            return

        knowledge_base = self._get_knowledge_base()

        if not knowledge_base:
            await send_embed(
                ctx,
                "Knowledge Base Empty",
                "The knowledge base is empty. Please add documents first.",
                discord.Color.orange(),
                "⚠️",
            )
            return

        try:
            self.active_requests.add(user_id)

            async with ctx.typing():
                answer, success = await self.ai_client.ask(
                    user_id, question, knowledge_base
                )

                if success:
                    color = discord.Color.green()
                    title = "AI Answer"
                    emoji = "🤖"
                else:
                    color = discord.Color.red()
                    title = "Error"
                    emoji = "❌"

                await send_embed(ctx, title, answer, color, emoji)

        except asyncio.CancelledError:
            logger.warning(f"Request from user {user_id} was cancelled")
            await send_embed(
                ctx,
                "Request Cancelled",
                "Your request was cancelled due to a server issue. Please try again.",
                discord.Color.red(),
                "🚫",
            )
        except Exception as e:
            logger.error(
                f"Unexpected error processing request from user {user_id}: {str(e)}"
            )
            await send_embed(
                ctx,
                "Unexpected Error",
                f"An unexpected error occurred: {str(e)}",
                discord.Color.red(),
                "💥",
            )
        finally:
            self.active_requests.remove(user_id)

    def _get_knowledge_base(self) -> List[Dict[str, str]]:
        if not self.nlp_cog or not hasattr(self.nlp_cog, "nlp_processor"):
            return []

        knowledge_base = []

        phrases = self.nlp_cog.nlp_processor.all_phrases
        answers = self.nlp_cog.nlp_processor.answer_map

        if not phrases or not answers:
            return []

        answer_to_phrases = {}
        for phrase, answer in zip(phrases, answers):
            if answer not in answer_to_phrases:
                answer_to_phrases[answer] = []
            answer_to_phrases[answer].append(phrase)

        for answer, related_phrases in answer_to_phrases.items():
            knowledge_base.append(
                {
                    "title": " | ".join(related_phrases[:3]),
                    "content": answer,
                }
            )

        return knowledge_base


async def setup(bot):
    await bot.add_cog(AI(bot))
