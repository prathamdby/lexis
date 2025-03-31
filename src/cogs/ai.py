import discord
from discord.ext import commands
import logging
from typing import List, Dict
import pandas as pd

from src.utils.helpers import send_embed
from src.utils.ai_client import AIClient

logger = logging.getLogger(__name__)


class AI(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ai_client = AIClient()
        self.nlp_cog = None

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

        # Get knowledge base from NLP cog
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

        # Show loading state
        async with ctx.typing():
            # Get answer from AI client
            answer, success = await self.ai_client.ask(
                ctx.author.id, question, knowledge_base
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

    def _get_knowledge_base(self) -> List[Dict[str, str]]:
        if not self.nlp_cog or not hasattr(self.nlp_cog, "nlp_processor"):
            return []

        # Create a knowledge base from NLP processor data
        knowledge_base = []

        # Get unique entries from answer_map with corresponding phrases
        phrases = self.nlp_cog.nlp_processor.all_phrases
        answers = self.nlp_cog.nlp_processor.answer_map

        if not phrases or not answers:
            return []

        # Create a dictionary mapping answers to their phrases
        answer_to_phrases = {}
        for phrase, answer in zip(phrases, answers):
            if answer not in answer_to_phrases:
                answer_to_phrases[answer] = []
            answer_to_phrases[answer].append(phrase)

        # Create knowledge base entries
        for answer, related_phrases in answer_to_phrases.items():
            knowledge_base.append(
                {
                    "title": " | ".join(
                        related_phrases[:3]
                    ),  # Use first few phrases as title
                    "content": answer,
                }
            )

        return knowledge_base


async def setup(bot):
    await bot.add_cog(AI(bot))
