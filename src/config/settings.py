import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
GUILD_ID = os.getenv("GUILD_ID")

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOGGING_CONFIG = {
    "version": 1,
    "formatters": {
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": LOG_LEVEL,
            "formatter": "standard",
        },
    },
    "loggers": {"": {"handlers": ["console"], "level": LOG_LEVEL, "propagate": True}},
}
