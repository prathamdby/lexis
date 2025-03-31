import discord
from discord.ext import commands, tasks
import logging
import time
import nltk
from src.utils.nlp_processor import NLPProcessor
from src.utils.helpers import has_role, send_embed
from src.config.settings import DATA_REFRESH_INTERVAL

logger = logging.getLogger(__name__)


class NLPCog(commands.Cog, name="NLP"):
    def __init__(self, bot):
        self.bot = bot
        self._initialize_nltk()
        self.nlp_processor = NLPProcessor()
        self.last_refresh = time.time()
        logger.info("NLP processor initialized")

    def _initialize_nltk(self):
        try:
            nltk.download("punkt", quiet=True)
            nltk.download("stopwords", quiet=True)
            logger.info("NLTK resources initialized")
        except Exception as e:
            logger.warning(f"Failed to initialize NLTK resources: {e}")

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("NLP cog loaded")
        self.periodic_refresh.start()

    def cog_unload(self):
        self.periodic_refresh.cancel()

    @tasks.loop(seconds=DATA_REFRESH_INTERVAL)
    async def periodic_refresh(self):
        logger.info("Refreshing NLP model data...")
        self.nlp_processor.process_data()
        self.last_refresh = time.time()
        logger.info("NLP model data refreshed")

    @periodic_refresh.before_loop
    async def before_refresh(self):
        await self.bot.wait_until_ready()

    async def process_message(self, message):
        answer, similarity = self.nlp_processor.find_best_match(message.content)
        if answer and similarity > 0.3:
            try:
                await message.reply(f"{answer}", suppress_embeds=True)
            except discord.Forbidden:
                await message.channel.send(f"{message.author.mention} {answer}")
                logger.warning(
                    f"Failed to reply to message from {message.author}: {message.content}"
                )
            finally:
                logger.info(
                    f"Matched query: '{message.content}' with similarity {similarity:.2f}"
                )

    @commands.command(
        name="update",
        description="Refresh response database from Google Sheets to get the latest answers",
    )
    @has_role()
    async def refresh_nlp(self, ctx):
        logger.info(f"{ctx.author} requested data refresh")
        await ctx.send("📡 Refreshing response database...")

        self.nlp_processor.process_data()
        self.last_refresh = time.time()

        fields = [
            {
                "name": "Database Size",
                "value": f"`{len(self.nlp_processor.all_phrases)}` trigger phrases loaded",
                "inline": False,
            },
            {
                "name": "Next Update",
                "value": f"<t:{int(self.last_refresh + DATA_REFRESH_INTERVAL)}:R>",
                "inline": False,
            },
        ]

        await send_embed(
            ctx,
            "Database Update Complete",
            "✅ Successfully refreshed response database from Google Sheets",
            discord.Color.green(),
            "🔄",
            fields,
        )

    @commands.command(
        name="status",
        description="Display system statistics including database size and update schedule",
    )
    @has_role()
    async def nlp_status(self, ctx):
        phrases_count = len(self.nlp_processor.all_phrases)

        fields = [
            {
                "name": "Database Size",
                "value": f"`{phrases_count}` trigger phrases",
                "inline": True,
            },
            {
                "name": "Last Update",
                "value": f"<t:{int(self.last_refresh)}:R>",
                "inline": True,
            },
            {
                "name": "Next Update",
                "value": f"<t:{int(self.last_refresh + DATA_REFRESH_INTERVAL)}:R>",
                "inline": True,
            },
            {
                "name": "Update Interval",
                "value": f"`{DATA_REFRESH_INTERVAL}` seconds",
                "inline": True,
            },
        ]

        await send_embed(
            ctx,
            "System Status Report",
            "Current status of the response system",
            discord.Color.blue(),
            "📊",
            fields,
        )

    @commands.command(
        name="responses",
        description="Show all configured trigger phrases and their corresponding responses",
    )
    @has_role()
    async def list_keywords(self, ctx):
        if not self.nlp_processor.all_phrases:
            await send_embed(
                ctx,
                "Empty Database",
                "No trigger phrases or responses found in the database.",
                discord.Color.red(),
                "⚠️",
            )
            return

        keyword_responses = {}
        for phrase, answer in zip(
            self.nlp_processor.all_phrases, self.nlp_processor.answer_map
        ):
            if answer in keyword_responses:
                keyword_responses[answer].append(phrase)
            else:
                keyword_responses[answer] = [phrase]

        embeds = []
        current_embed = discord.Embed(
            title="Response Configuration",
            description="List of available responses and their trigger phrases",
            color=discord.Color.blue(),
        )
        current_embed.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.avatar.url if ctx.author.avatar else None,
        )
        current_length = 0

        for answer, keywords in keyword_responses.items():
            field_content = ", ".join([f"`{k}`" for k in keywords])
            if current_length + len(field_content) + len(answer) > 5500:
                embeds.append(current_embed)
                current_embed = discord.Embed(
                    title="Response Configuration (Continued)",
                    color=discord.Color.blue(),
                )
                current_length = 0

            current_embed.add_field(
                name=f"📝 {answer[:250]}" if len(answer) > 250 else f"📝 {answer}",
                value=(
                    f"Triggers: {field_content[:1020]}"
                    if len(field_content) > 1020
                    else f"Triggers: {field_content}"
                ),
                inline=False,
            )
            current_length += len(field_content) + len(answer)

        if len(current_embed.fields) > 0:
            embeds.append(current_embed)

        for i, embed in enumerate(embeds):
            embed.set_footer(text=f"Page {i+1}/{len(embeds)} | {ctx.bot.user.name}")
            await ctx.send(embed=embed)

    @commands.command(
        name="test", description="Test how the bot would respond to a specific message"
    )
    @has_role()
    async def test_query(self, ctx, *, query=None):
        if not query:
            await send_embed(
                ctx,
                "Missing Query",
                "Please provide a message to test.",
                discord.Color.red(),
                "❌",
            )
            return

        answer, similarity = self.nlp_processor.find_best_match(query)

        if answer:
            fields = [
                {"name": "Test Message", "value": f"`{query}`", "inline": False},
                {"name": "Response", "value": answer, "inline": False},
                {
                    "name": "Match Confidence",
                    "value": f"`{similarity:.2%}`",
                    "inline": True,
                },
            ]

            await send_embed(
                ctx,
                "Test Results",
                "✅ Found matching response",
                discord.Color.green(),
                "🔍",
                fields,
            )
        else:
            await send_embed(
                ctx,
                "No Match Found",
                f"No suitable response found for: `{query}`",
                discord.Color.red(),
                "❌",
            )


async def setup(bot):
    await bot.add_cog(NLPCog(bot))
