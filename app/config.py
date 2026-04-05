from __future__ import annotations

import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path

DATABASE_URL = os.environ.get(
    "DATABASE_URL", "postgresql://kitsune:kitsune@localhost:5432/kitsune"
)

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
LOG_FILE = DATA_DIR / "kitsune.log"


def setup_logging() -> None:
    DATA_DIR.mkdir(exist_ok=True)
    handler = RotatingFileHandler(LOG_FILE, maxBytes=5_000_000, backupCount=3)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
    )
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.DEBUG)
    app_logger.addHandler(handler)
