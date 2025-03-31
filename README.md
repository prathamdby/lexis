# Lexis Discord Bot

🗣️ Lexis is an intelligent Discord bot that uses Natural Language Processing (NLP) to provide automated responses based on a configurable knowledge base. It features a sophisticated modular design, comprehensive administrative controls, and real-time response matching capabilities.

## Features

### Core Functionality

- Advanced real-time message analysis using NLP:
  - TF-IDF vectorization with cosine similarity matching
  - Intelligent message preprocessing (tokenization and stopword removal)
  - Configurable similarity thresholds for response matching
- Dynamic response database via Google Sheets integration with automatic updates
- Role-based access control with owner override capabilities

### System Features

- Periodic data refresh system with configurable intervals
- Comprehensive logging system with configurable levels
- Modular architecture using Discord.py cogs
- Real-time bot status updates
- System health monitoring and latency tracking
- Professional embed messages with consistent formatting and emojis

## Setting up the Bot

Follow these steps to configure your bot:

1. Visit [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application and add a bot
3. Enable required intents (Message Content, Server Members)
4. Copy the bot token
5. Configure your .env file using the template below:

```env
# Discord Bot Configuration
BOT_TOKEN=your_discord_bot_token_here
BOT_PREFIX=!
ADMIN_ROLE=Bot Admin
OWNER_ID=your_discord_user_id_here

# Application Configuration
LOG_LEVEL=INFO

# NLP Configuration
GOOGLE_SHEET_ID=your_sheet_id_here
DATA_REFRESH_INTERVAL=600
```

## Available Commands

### Admin Commands

- `!reload` - Reload all bot modules to apply code changes
  - Provides detailed success/failure report for each module
  - Maintains bot stability during updates
- `!shutdown` - Safely shutdown the bot and save all states
  - Ensures clean termination of all processes
  - Logs shutdown event for monitoring
- `!restart` - Restart the bot process
  - Automatically reinitializes all systems
  - Maintains configurations and states

### NLP Commands

- `!update` - Refresh response database from Google Sheets
  - Force-updates the NLP model with latest data
  - Displays current database size and next scheduled update
- `!status` - Display system statistics and update schedule
  - Shows database size and update timestamps
  - Monitors refresh intervals and system health
- `!responses` - Show all configured trigger phrases and their responses
  - Paginates large response sets automatically
  - Groups triggers by response for better organization
- `!test <message>` - Test how the bot would respond to a specific message
  - Shows match confidence scores
  - Displays exact response that would be sent

### Basic Commands

- `!ping` - Check bot's connection health and response times
  - Monitors both Gateway and API latency
  - Provides visual status indicators
  - Alerts on high latency conditions

## Tech Stack

- **Framework**: discord.py ≥2.5.2

  - Asynchronous operation
  - Event-driven architecture
  - Comprehensive Discord API support

- **NLP Processing**:

  - NLTK ≥3.9.1 for text processing
    - Tokenization
    - Stopword removal
  - scikit-learn ≥1.6.1 for text analysis
    - TF-IDF vectorization
    - Cosine similarity computation
  - pandas ≥2.2.3 for data handling
  - numpy ≥2.2.4 for numerical operations

- **Configuration**:

  - python-dotenv ≥1.1.0 for environment management
  - Centralized settings module

- **Integrations**:

  - Google Sheets for dynamic data sourcing
  - Automatic data refresh mechanism

- **Logging**:
  - Structured logging with configurable levels
  - Comprehensive error tracking
  - Activity monitoring

## Project Structure

```
src/
├── cogs/           # Feature modules
│   ├── admin.py    # Administrative commands and controls
│   ├── basic.py    # System health and utility commands
│   ├── nlp.py      # Core NLP functionality and commands
│   └── tasks.py    # Background tasks and status updates
├── config/         # Settings and configuration
│   └── settings.py # Centralized configuration management
├── utils/          # Utility modules
│   ├── helpers.py  # Common utilities and decorators
│   └── nlp_processor.py  # NLP engine implementation
└── main.py         # Bot initialization and core setup
```

## Getting Started

1. Ensure Python ≥3.11 is installed
2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Configure your .env file with required credentials
4. Start the bot:

```bash
python run.py
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.
