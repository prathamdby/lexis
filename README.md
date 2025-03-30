# Lexis Discord Bot

Lexis is an intelligent Discord bot that uses Natural Language Processing (NLP) to provide automated responses based on a configurable knowledge base. It features a modular design, administrative controls, and real-time response matching capabilities.

## Features

- Real-time message analysis using NLP
- Dynamic response database via Google Sheets integration
- Automatic data refresh system
- Role-based access control
- Command-based administration
- Professional embed messages with consistent formatting
- Comprehensive logging system
- Modular architecture for easy expansion

## Setting up the Bot

Follow these steps to configure your bot:

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and add a bot
3. Copy the bot token
4. Configure your .env file using the template below:

```env
# Discord Bot Configuration
BOT_TOKEN=your_discord_bot_token_here
BOT_PREFIX=!
ADMIN_ROLE=Bot Admin

# Application Configuration
LOG_LEVEL=INFO

# NLP Configuration
GOOGLE_SHEET_ID=your_sheet_id_here
DATA_REFRESH_INTERVAL=600
```

## Available Commands

### Admin Commands

- `!reload` - Reload all bot modules to apply code changes
- `!shutdown` - Safely shutdown the bot and save all states

### NLP Commands

- `!update` - Refresh response database from Google Sheets
- `!status` - Display system statistics and update schedule
- `!responses` - Show all configured trigger phrases
- `!test <message>` - Test how the bot would respond to a specific message

### Basic Commands

- `!ping` - Check bot's connection health and response times

## Tech Stack

- **Framework**: discord.py - Advanced Discord bot framework
- **NLP Processing**:
  - NLTK for text processing
  - scikit-learn for TF-IDF vectorization
  - pandas for data handling
- **Configuration**: python-dotenv
- **Integrations**: Google Sheets API
- **Logging**: Python's built-in logging module

## Project Structure

```
src/
├── cogs/         # Feature modules
│   ├── admin.py  # Administrative commands
│   ├── basic.py  # Basic utility commands
│   ├── nlp.py    # NLP functionality
│   └── tasks.py  # Background tasks
├── config/       # Settings and configuration
├── utils/        # Helper functions and NLP processor
└── main.py       # Bot entry point
```

## Getting Started

First, install the required dependencies:

```bash
pip install -r requirements.txt
```

Then start the bot:

```bash
python run.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
