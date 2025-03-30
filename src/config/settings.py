import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_PREFIX = os.getenv("BOT_PREFIX", "!")
ADMIN_ROLE = os.getenv("ADMIN_ROLE", "Bot Admin")
OWNER_ID = int(os.getenv("OWNER_ID", "0"))

GOOGLE_SHEET_ID = os.getenv("GOOGLE_SHEET_ID", "")
GOOGLE_SHEET_URL = (
    f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/export?format=csv"
    if GOOGLE_SHEET_ID
    else ""
)
DATA_REFRESH_INTERVAL = int(os.getenv("DATA_REFRESH_INTERVAL", 600))

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
