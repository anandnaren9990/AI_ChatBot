import logging
import os
from logging.handlers import RotatingFileHandler

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

file_handler = RotatingFileHandler(
    filename=f"{log_dir}/app.log",
    maxBytes=3*1024*1024,
    backupCount=3
)

stream_handler = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    handlers=[file_handler,stream_handler]
)

logger = logging.getLogger("Ai Chat bot")