import discord
from discord.ext import commands
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

    async def process_message(self, message):
        self.nlp_processor.update_model_if_needed()

        answer, similarity = self.nlp_processor.find_best_match(message.content)
        if answer and similarity > 0.3:
            await message.reply(f"{answer}")
            logger.info(
                f"Matched query: '{message.content}' with similarity {similarity:.2f}"
            )

    @commands.command(
        name="refresh_nlp", description="Refresh NLP data from Google Sheets"
    )
    @has_role("Bot Admin")
    async def refresh_nlp(self, ctx):
        logger.info(f"{ctx.author} requested data refresh")
        await ctx.send("Refreshing NLP data...")

        self.nlp_processor.process_data()
        self.nlp_processor.last_data_refresh = time.time()

        await send_embed(
            ctx,
            "NLP Data Refreshed",
            f"Successfully loaded {len(self.nlp_processor.all_phrases)} phrases for matching.",
            discord.Color.green(),
        )

    @commands.command(name="nlp_status", description="Show NLP system status")
    @has_role("Bot Admin")
    async def nlp_status(self, ctx):
        phrases_count = len(self.nlp_processor.all_phrases)
        last_refresh = time.ctime(self.nlp_processor.last_data_refresh)
        next_refresh = time.ctime(
            self.nlp_processor.last_data_refresh + DATA_REFRESH_INTERVAL
        )

        status_text = (
            f"**Phrases in database:** {phrases_count}\n"
            f"**Last refresh:** {last_refresh}\n"
            f"**Next refresh due:** {next_refresh}\n"
            f"**Refresh interval:** {DATA_REFRESH_INTERVAL} seconds"
        )

        await send_embed(ctx, "NLP System Status", status_text, discord.Color.blue())

    @commands.command(
        name="list_keywords", description="List all keywords and their responses"
    )
    @has_role("Bot Admin")
    async def list_keywords(self, ctx):
        if not self.nlp_processor.all_phrases:
            await send_embed(
                ctx,
                "No Keywords Found",
                "There are currently no keywords in the database.",
                discord.Color.red(),
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
            title="Keywords and Responses",
            description="All available keywords and their corresponding responses:",
            color=discord.Color.blue(),
        )
        current_length = 0

        for answer, keywords in keyword_responses.items():
            field_content = ", ".join(keywords)
            if current_length + len(field_content) + len(answer) > 5500:
                embeds.append(current_embed)
                current_embed = discord.Embed(
                    title="Keywords and Responses (Continued)",
                    color=discord.Color.blue(),
                )
                current_length = 0

            current_embed.add_field(
                name=(
                    f"Response: {answer[:250]}"
                    if len(answer) > 250
                    else f"Response: {answer}"
                ),
                value=(
                    f"Keywords: {field_content[:1020]}"
                    if len(field_content) > 1020
                    else f"Keywords: {field_content}"
                ),
                inline=False,
            )
            current_length += len(field_content) + len(answer)

        if len(current_embed.fields) > 0:
            embeds.append(current_embed)

        for i, embed in enumerate(embeds):
            embed.set_footer(text=f"Page {i+1}/{len(embeds)}")
            await ctx.send(embed=embed)

    @commands.command(
        name="test_query", description="Test a query against the NLP system"
    )
    @has_role("Bot Admin")
    async def test_query(self, ctx, *, query=None):
        if not query:
            await ctx.send("Please provide a query to test.")
            return

        self.nlp_processor.update_model_if_needed()
        answer, similarity = self.nlp_processor.find_best_match(query)

        if answer:
            embed = discord.Embed(
                title="Query Match Results", color=discord.Color.green()
            )
            embed.add_field(name="Query", value=query, inline=False)
            embed.add_field(name="Answer", value=answer, inline=False)
            embed.add_field(
                name="Similarity Score", value=f"{similarity:.4f}", inline=False
            )
            await ctx.send(embed=embed)
        else:
            await send_embed(
                ctx,
                "No Match Found",
                f"No match found for query: '{query}'",
                discord.Color.red(),
            )


async def setup(bot):
    await bot.add_cog(NLPCog(bot))
