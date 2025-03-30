# Lexis - Modular Discord Bot

A fully featured, scalable, and modular Discord bot built with discord.py. This bot implements a modular cog-based architecture for easy feature expansion.

## Features

- Modular cog-based architecture for easy feature management
- Support for both prefix commands and slash commands
- Dynamic loading, unloading, and reloading of cogs
- Role-based access control for administrative commands
- Background tasks for status rotation and maintenance
- Comprehensive error handling and logging
- Secure environment variable management

## Setup

### Prerequisites

- Python 3.8 or higher
- Discord.py 2.3.2 or higher
- A Discord Bot Token

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/lexis.git
cd lexis
```

2. Set up a virtual environment using uv:
```bash
pip install uv
uv venv
```

3. Activate the virtual environment:
```bash
# On Windows
.venv\Scripts\activate
# On macOS/Linux
source .venv/bin/activate
```

4. Install dependencies using uv:
```bash
uv pip install -r requirements.txt
```

5. Create a `.env` file in the root directory with your bot token:
```
BOT_TOKEN=your_discord_bot_token_here
BOT_PREFIX=!
GUILD_ID=your_guild_id_here
LOG_LEVEL=INFO
```

### Running the Bot

```bash
# Run from the project root directory
python run.py

# Alternatively, you can use uv
uv run run.py
```

## Bot Commands

### Basic Commands
- `!ping` - Check bot latency
- `!info` - Display server information
- `!help` - Display available commands

### Admin Commands (requires "Bot Admin" role)
- `!load <cog>` - Load a cog
- `!unload <cog>` - Unload a cog
- `!reload <cog>` - Reload a cog
- `!shutdown` - Shutdown the bot

## Adding New Features

To add a new feature to the bot, create a new cog file in the `src/cogs` directory. The bot will automatically load all cogs in this directory.

Example cog structure:

```python
import discord
from discord.ext import commands

class MyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print("MyCog loaded")
    
    @commands.command(name="mycommand")
    async def my_command(self, ctx):
        await ctx.send("Hello from my command!")

async def setup(bot):
    await bot.add_cog(MyCog(bot))
```

## License

MIT

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit your changes: `git commit -m 'Add some feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request
